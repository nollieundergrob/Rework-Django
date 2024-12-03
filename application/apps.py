from django.apps import AppConfig

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'

    def ready(self):
        # Убедитесь, что файл signals.py существует, или уберите следующую строку
        try:
            import application.signals
        except ImportError:
            pass
