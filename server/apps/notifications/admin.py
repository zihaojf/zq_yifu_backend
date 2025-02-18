from django.contrib import admin

from .models import Notifications


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("send_time", "message", "send_user", "receive_user")
    list_filter = ("send_time", "send_user", "receive_user")
    search_fields = ("send_time", "message")
    ordering = ("send_time",)
