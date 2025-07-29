from django.apps import AppConfig

class MessagesConfig(AppConfig):
    name = 'messages'

    def ready(self):
        import messages.signals
