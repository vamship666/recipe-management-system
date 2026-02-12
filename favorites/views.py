from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Favourite


class FavouriteViewSet(viewsets.ModelViewSet):
    # ViewSet to manage favourite records
    queryset = Favourite.objects.all()

    # Only authenticated users can access favourites
    permission_classes = [IsAuthenticated]
