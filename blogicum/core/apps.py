"""Application configuration for shared project components."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configure the core application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
