from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Define available user roles
    ROLE_CHOICES = (
        ('creator', 'Creator'),
        ('viewer', 'Viewer'),
    )

    # Role field to differentiate creators and viewers
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        # Return username for readable representation
        return self.username
