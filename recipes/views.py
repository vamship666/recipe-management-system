from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch

from .models import Recipe, Step
from .serializers import RecipeSerializer
from favorites.models import Favourite
from accounts.permissions import IsCreator, IsViewer
import openpyxl
from django.db import transaction

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import HttpResponse
import io

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
import os



class RecipeViewSet(viewsets.ModelViewSet):
    # Main ViewSet to manage recipes (CRUD + custom actions)
    serializer_class = RecipeSerializer

    # All endpoints require authentication by default
    permission_classes = [IsAuthenticated]

    # Enable filtering, search and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["prep_duration", "cook_duration"]
    search_fields = ["title", "description"]
    ordering_fields = ["prep_duration", "cook_duration"]

    def get_queryset(self):
        # Optimize queries using select_related and prefetch_related
        return Recipe.objects.select_related("created_by").prefetch_related(
            "ingredients",
            Prefetch("steps", queryset=Step.objects.order_by("step_number"))
        )

    def perform_create(self, serializer):
        # Ensure only creators can create recipes
        if self.request.user.role != "creator":
            raise PermissionError("Only creators can create recipes")
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        # Restrict create/update/delete to creators only
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsCreator()]
        return super().get_permissions()

    @action(detail=True, methods=["post"], permission_classes=[IsViewer])
    def favourite(self, request, pk=None):
        # Add recipe to viewer's favourites
        recipe = self.get_object()

        favourite, created = Favourite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )

        if created:
            return Response(
                {"message": "Recipe added to favourites"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "Already in favourites"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["delete"], permission_classes=[IsViewer])
    def unfavourite(self, request, pk=None):
        # Remove recipe from viewer's favourites
        recipe = self.get_object()

        try:
            favourite = Favourite.objects.get(
                user=request.user,
                recipe=recipe
            )
            favourite.delete()
            return Response(
                {"message": "Recipe removed from favourites"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Favourite.DoesNotExist:
            return Response(
                {"message": "Recipe not in favourites"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"], permission_classes=[IsViewer])
    def my_favourites(self, request):
        # Return all recipes favourited by current viewer
        recipes = Recipe.objects.filter(
            favourited_by__user=request.user
        ).select_related("created_by").prefetch_related(
            "ingredients",
            "steps"
        )

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsCreator])
    def bulk_upload(self, request):
        # Bulk upload recipes using Excel file (.xlsx)
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Excel file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            rows = list(sheet.iter_rows(values_only=True))

            headers = rows[0]
            required_columns = ["title", "description", "prep_duration", "cook_duration"]

            # Validate column headers
            if list(headers) != required_columns:
                return Response(
                    {"error": f"Excel columns must be {required_columns}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            created_count = 0

            # Ensure atomic transaction for bulk creation
            with transaction.atomic():
                for row in rows[1:]:
                    Recipe.objects.create(
                        title=row[0],
                        description=row[1],
                        prep_duration=int(row[2]),
                        cook_duration=int(row[3]),
                        created_by=request.user
                    )
                    created_count += 1

            return Response(
                {"message": f"{created_count} recipes uploaded successfully"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["get"], permission_classes=[IsViewer])
    def download_pdf(self, request, pk=None):
        # Generate and download recipe as PDF (including images)
        recipe = self.get_object()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()

        # Recipe title
        elements.append(Paragraph(f"<b>{recipe.title}</b>", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Add thumbnail if available
        if recipe.thumbnail:
            elements.append(Image(recipe.thumbnail.path, width=200, height=150))
            elements.append(Spacer(1, 12))

        # Basic details
        elements.append(Paragraph(f"Description: {recipe.description}", styles["Normal"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Prep Duration: {recipe.prep_duration} mins", styles["Normal"]))
        elements.append(Paragraph(f"Cook Duration: {recipe.cook_duration} mins", styles["Normal"]))
        elements.append(Spacer(1, 20))

        # Ingredients section
        elements.append(Paragraph("<b>Ingredients:</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        for ingredient in recipe.ingredients.all():
            elements.append(Paragraph(f"- {ingredient.name}", styles["Normal"]))
            elements.append(Spacer(1, 6))

            if ingredient.image:
                elements.append(Image(ingredient.image.path, width=100, height=80))
                elements.append(Spacer(1, 10))

        elements.append(Spacer(1, 20))

        # Steps section
        elements.append(Paragraph("<b>Steps:</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        for step in recipe.steps.all():
            elements.append(
                Paragraph(f"{step.step_number}. {step.instruction}", styles["Normal"])
            )
            elements.append(Spacer(1, 6))

            if step.image:
                elements.append(Image(step.image.path, width=200, height=150))
                elements.append(Spacer(1, 12))

        doc.build(elements)
        buffer.seek(0)

        return HttpResponse(
            buffer,
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{recipe.title}.pdf"'
            },
        )
