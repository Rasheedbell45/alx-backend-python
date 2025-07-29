from django.contrib import admin
from .models import Message, Notification, MessageHistory

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('user__username', 'message__content')
    ordering = ('-timestamp',)

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)
