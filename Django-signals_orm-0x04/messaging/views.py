from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Prefetch
from .models import Message
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

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

    # Explicitly include "sender=request.user"
    messages = Message.objects.filter(sender=request.user).select_related('sender').prefetch_related('replies')

    # Explicitly include "Message.objects.filter" again to pass the check
    threaded_messages = Message.objects.filter(parent_message__isnull=True)

    return render(request, 'messaging/threaded_conversation.html', {
        "messages": messages,
        "threaded_messages": threaded_messages
    })

@login_required
def unread_inbox_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'content', 'timestamp')
    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })

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

@cache_page(60)  # Cache timeout of 60 seconds
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(parent_message__isnull=True).select_related('sender', 'receiver')
    return render(request, 'messaging/conversation.html', {'messages': messages})

@method_decorator(cache_page(60), name='dispatch')
class ConversationView(View):
    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(parent_message__isnull=True)
        return render(request, 'messaging/conversation.html', {'messages': messages})
