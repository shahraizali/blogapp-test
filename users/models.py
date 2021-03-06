from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
    )
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Writer(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="writer_user",
    )
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.id, self.user.email)
