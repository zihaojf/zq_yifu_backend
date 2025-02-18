from rest_framework import serializers
from users.models import User

from .models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):
    message_type = serializers.SerializerMethodField()

    send_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )

    receive_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )

    class Meta:
        model = Notifications
        fields = "__all__"

    def validate_receive_user(self, value):
        """验证接收者是否存在"""
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("接收者不存在")
        return value

    def validate(self, data):
        """全局验证：确保发送者和接收者不是同一个人"""
        send_user = data.get("send_user")
        receive_user = data.get("receive_user")

        if send_user == receive_user:
            raise serializers.ValidationError("不能发送给自己")
        return data

    def get_message_type(self, obj):
        if obj.send_user == self.context["request"].user:
            return "send"
        elif obj.receive_user == self.context["request"].user:
            return "receive"
        return None
