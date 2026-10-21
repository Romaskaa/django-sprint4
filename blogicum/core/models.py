"""Abstract models shared by project applications."""

from django.db import models


class BaseModel(models.Model):
    """Base model with common fields for all models."""

    is_published = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
        verbose_name="Добавлено",
    )

    class Meta:
        """Declare the model as abstract."""

        abstract = True
