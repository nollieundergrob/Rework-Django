from django.apps import AppConfig


class LocalpypiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'localpypi'
    def ready(self):
        import localpypi.signals