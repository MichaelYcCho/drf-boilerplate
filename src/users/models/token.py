from django.db import models

from core.models import TimeStamp


class TokenStorage(TimeStamp):
    refresh_token = models.CharField(
        max_length=255,
        null=True,
    )
    refresh_token_expired_at = models.IntegerField(
        null=True,
    )
    user = models.OneToOneField(
        "User",
        related_name="token_storage",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "users_token_storage"
