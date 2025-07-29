from django.apps import AppConfig

class MessagesConfig(AppConfig):
    name = 'messages'

    def ready(self):
        import messages.signals

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        import messaging.signals
