from django.apps import AppConfig


class VideoPlatformAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_platform_app'

    def ready(self):
        from . import signals
        return super().ready()
