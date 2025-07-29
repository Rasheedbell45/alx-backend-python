from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message
from notifications.models import Notification

class MessageNotificationTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password123')
        self.receiver = User.objects.create_user(username='receiver', password='password123')

    def test_message_creation_triggers_notification(self):
        # Ensure no notifications exist at first
        self.assertEqual(Notification.objects.count(), 0)

        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello!'
        )

        # There should now be one notification for the receiver
        self.assertEqual(Notification.objects.count(), 1)

        # Check the notification details
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_multiple_messages_create_multiple_notifications(self):
        Message.objects.create(sender=self.sender, receiver=self.receiver, content='Message 1')
        Message.objects.create(sender=self.sender, receiver=self.receiver, content='Message 2')

        self.assertEqual(Notification.objects.count(), 2)
