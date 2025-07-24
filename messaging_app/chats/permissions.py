from rest_framework import permissions

class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to only allow users involved in a conversation or 
    sender/receiver of a message to access it.
    """

    def has_object_permission(self, request, view, obj):
        # For Message object: allow if sender or receiver is the user
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == request.user or obj.receiver == request.user

        # For Conversation object: allow if user is in participants
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False

from rest_framework.permissions import IsAuthenticated
from chats.permissions import IsParticipantOrSender

class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOrSender]

from rest_framework.viewsets import ModelViewSet
from chats.permissions import IsParticipantOrSender

class ConversationViewSet(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOrSender]

class MessageListView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

  class ConversationListView(ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)
