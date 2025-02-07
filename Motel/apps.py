from django.apps import AppConfig


class MotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Motel'

    def ready(self):
        import Motel.signals
