from django.contrib import admin

from .models import MoveRecord


@admin.register(MoveRecord)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "move_user", "moved_user", "move_vehicle")
    search_fields = ("id",)
    list_filter = ("move_user", "moved_user", "move_vehicle")
    ordering = ("move_time",)
