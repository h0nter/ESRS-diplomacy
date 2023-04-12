from django.apps import AppConfig


class HostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'host'

    def ready(self):
        import host.signals  # noqa
