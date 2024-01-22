from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUserModel(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    age = models.IntegerField(null=True, blank=None)
    country = models.CharField(max_length=50, null=True, blank=None)
    user_credits = models.IntegerField(default=0)
