from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Prefetch
from .models import Message
from django.shortcuts import render

def get_all_replies(message):
    replies = message.replies.all().select_related('sender')
    all_replies = []
    for reply in replies:
        all_replies.append(reply)
        all_replies += get_all_replies(reply)  # recursively fetch child replies
    return all_replies

@login_required
def threaded_conversation_view(request):
    user = request.user
    top_level_messages = (
        Message.objects
        .filter(receiver=user, parent_message__isnull=True)
        .select_related('sender', 'receiver')  # optimize FK access
        .prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'receiver')
            )
        )
    )
    
    def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been successfully deleted.")
    return redirect('home')

    conversation_data = []
    for message in top_level_messages:
        conversation_data.append({
            "message": message,
            "replies": get_all_replies(message)
        })

    return render(request, 'messaging/threaded_conversation.html', {
        "conversations": conversation_data
    })
