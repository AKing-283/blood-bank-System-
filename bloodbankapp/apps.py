from django.apps import AppConfig

class BloodbankappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodbankapp'

    def ready(self):
        import bloodbankapp.signals
