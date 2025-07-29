from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been successfully deleted.")
    return redirect('home')
