from rest_framework import serializers
from users.models import User
from vehicle.models import Vehicle

from .models import MoveRecord


class MoveRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveRecord
        fields = "__all__"
        ordering = ["-move_time"]

    move_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )
    moved_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )
    move_vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        required=True,
    )
