from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "user", "charging_time")
    search_fields = ("name", "code")
    list_filter = ("user",)
    ordering = ("charging_time",)
