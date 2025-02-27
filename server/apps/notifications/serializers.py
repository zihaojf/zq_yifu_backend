from rest_framework import serializers
from users.models import User

from .models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):
    message_type = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    opposite_username = serializers.SerializerMethodField()

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
        read_only_fields = ["avatar"]

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
        """动态设置消息类型：发送还是接收"""
        if obj.send_user == self.context["request"].user:
            return "send"
        elif obj.receive_user == self.context["request"].user:
            return "receive"
        return None

    def get_avatar(self, obj):
        """动态设置返回对方用户头像"""
        current_user = self.context["request"].user
        if current_user == obj.send_user:
            opposite_user = obj.receive_user
        elif current_user == obj.receive_user:
            opposite_user = obj.send_user
        else:
            return None

        if (
            opposite_user
            and hasattr(opposite_user, "avatar")
            and opposite_user.avatar
        ):
            request = self.context["request"]
            return (
                request.build_absolute_uri(opposite_user.avatar.url)
                if request
                else opposite_user.avatar.url
            )
        return None

    def get_opposite_username(self, obj):
        """获取对方用户昵称"""
        current_user = self.context["request"].user
        if current_user == obj.send_user:
            opposite_user = obj.receive_user
        elif current_user == obj.receive_user:
            opposite_user = obj.send_user
        else:
            return None
        if (
            opposite_user
            and hasattr(opposite_user, "nickname")
            and opposite_user.nickname
        ):
            return opposite_user.nickname
        return None


class ReadNotificationsSerializer(serializers.ModelSerializer):
    opposite_user = serializers.IntegerField()

    class Meta:
        model = Notifications
        fields = ["send_user", "receive_user", "read_status", "opposite_user"]
        read_only_fields = ["send_user", "receive_user", "read_status"]

    def validate_opposite_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("用户不存在")
        return value
