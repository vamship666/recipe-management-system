from rest_framework import serializers
from .models import Recipe, Ingredient, Step


class IngredientSerializer(serializers.ModelSerializer):
    # Serializer for ingredient details
    class Meta:
        model = Ingredient
        fields = ["id", "name", "image"]


class StepSerializer(serializers.ModelSerializer):
    # Serializer for individual recipe steps
    class Meta:
        model = Step
        fields = ["id", "step_number", "instruction", "image"]


class RecipeSerializer(serializers.ModelSerializer):
    # Nested serializers for ingredients and steps
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)

    # Display creator username instead of full user object
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "prep_duration",
            "cook_duration",
            "thumbnail",
            "created_by",
            "ingredients",
            "steps",
        ]

    def create(self, validated_data):
        # Extract nested ingredients and steps data
        ingredients_data = validated_data.pop("ingredients")
        steps_data = validated_data.pop("steps")

        # Create recipe instance
        recipe = Recipe.objects.create(**validated_data)

        # Add or create ingredients and associate with recipe
        for ingredient_data in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data)
            recipe.ingredients.add(ingredient)

        # Create step instances linked to recipe
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        return recipe
