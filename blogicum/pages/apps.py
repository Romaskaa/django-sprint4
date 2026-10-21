"""Application configuration for static pages."""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Configure the static pages application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
