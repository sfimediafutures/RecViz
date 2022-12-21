from django.apps import AppConfig


class HandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'handler'

    def ready(self):
        from .signals import signals
