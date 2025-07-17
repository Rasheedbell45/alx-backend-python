from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'is_read']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        """Returns serialized messages in the conversation"""
        messages = obj.messages.all().order_by('-sent_at')
        return MessageSerializer(messages, many=True).data

    def validate(self, attrs):
        """Example of using serializers.ValidationError"""
        if 'participants' in attrs and len(attrs['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return attrs
