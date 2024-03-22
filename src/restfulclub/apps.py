from django.apps import AppConfig


class RestfulclubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restfulclub'

    def ready(self):
        import restfulclub.signals
