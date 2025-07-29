from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Prefetch
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been successfully deleted.")
    return redirect('home')

def get_threaded_conversation(user):
    top_level_messages = (
        Message.objects
        .filter(receiver=user, parent_message__isnull=True)
        .select_related('sender', 'receiver')  # Efficient foreign key access
        .prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender').order_by('timestamp')
            )
        )
        .order_by('-timestamp')
    )
    return top_level_messages
