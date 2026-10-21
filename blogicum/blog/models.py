"""Database models for the blog application."""

from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    """A category used to group blog posts."""

    title = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name="Заголовок",
    )
    description = models.TextField(blank=False, verbose_name="Описание")
    slug = models.SlugField(
        null=False,
        unique=True,
        blank=False,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        """Set human-readable model names."""

        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Return the category title."""
        return self.title


class Location(BaseModel):
    """A geographical location associated with blog posts."""

    name = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name="Название места",
    )

    class Meta:
        """Set human-readable model names."""

        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        """Return the location name."""
        return self.name


class Post(BaseModel):
    """A blog publication."""

    title = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name="Заголовок",
    )
    text = models.TextField(null=False, blank=False, verbose_name="Текст")
    pub_date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — можно делать "
            "отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Категория",
    )

    class Meta:
        """Set human-readable model names."""

        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ('-pub_date',)

    def __str__(self):
        """Return the post title."""
        return self.title
