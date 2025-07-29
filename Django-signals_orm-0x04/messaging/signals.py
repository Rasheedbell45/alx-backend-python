from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from django.db.models.signals import pre_save
from .models import Message, MessageHistory, Notification
from notifications.models import Notification

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Save old content in history
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.edited = True  # Mark as edited
        except Message.DoesNotExist:
            pass


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
