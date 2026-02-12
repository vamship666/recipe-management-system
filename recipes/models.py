from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    # Name of the ingredient
    name = models.CharField(max_length=255)

    # Optional image representing the ingredient
    image = models.ImageField(upload_to="ingredients/", null=True, blank=True)

    def __str__(self):
        # Return ingredient name for readable representation
        return self.name


class Recipe(models.Model):
    # Basic recipe details
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Duration fields in minutes
    prep_duration = models.PositiveIntegerField()
    cook_duration = models.PositiveIntegerField()

    # Optional thumbnail image for the recipe
    thumbnail = models.ImageField(upload_to="recipes/", null=True, blank=True)

    # User who created the recipe
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes"
    )

    # Many-to-many relationship with ingredients
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        # Return recipe title for readability
        return self.title


class Step(models.Model):
    # Each step belongs to a specific recipe
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="steps"
    )

    # Order of the step in the recipe
    step_number = models.PositiveIntegerField()

    # Instruction text for the step
    instruction = models.TextField()

    # Optional image for the step
    image = models.ImageField(upload_to="steps/", null=True, blank=True)

    class Meta:
        # Ensure steps are ordered by step number
        ordering = ["step_number"]

    def __str__(self):
        # Readable representation in admin
        return f"{self.recipe.title} - Step {self.step_number}"
