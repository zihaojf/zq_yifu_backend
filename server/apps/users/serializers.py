from django.contrib.auth.hashers import make_password
from rest_framework import serializers

# from urllib3 import request
from users.models import User

# from wechatpy.client.api import user


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",  # 用户 ID
            "username",
            "openid",  # 微信 openid
            "union_id",  # 自强 union_id
            "nickname",  # 昵称
            "phone",  # 手机号
            "faculty",  # 学部
            "avatar",  # 头像
            "credit_score",  # 信用分
            "password",  # 密码
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "openid": {"read_only": True},
            "union_id": {"read_only": True},
        }

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get("request")
            return (
                request.build_absolute_uri(obj.avatar.url)
                if request
                else obj.avatar.url
            )
        return None

    def validate_password(self, value):
        return make_password(value)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
