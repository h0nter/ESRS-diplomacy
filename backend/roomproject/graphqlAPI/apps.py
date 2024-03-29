from django.apps import AppConfig


class GraphqlapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphqlAPI'
    def ready(self):
        import graphqlAPI.signals  # noqa
