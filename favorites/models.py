from django.db import models
from django.conf import settings
from recipes.models import Recipe


class Favourite(models.Model):
    # Link favourite to a user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites"
    )

    # Link favourite to a recipe
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favourited_by"
    )

    # Timestamp when recipe was marked as favourite
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate favourites for same user & recipe
        unique_together = ("user", "recipe")

    def __str__(self):
        # Readable representation in admin
        return f"{self.user.username} -> {self.recipe.title}"
