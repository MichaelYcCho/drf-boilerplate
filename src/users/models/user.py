from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    email = models.CharField(
        max_length=100,
    )
    phone = models.CharField(
        max_length=20,
    )

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users_user"
