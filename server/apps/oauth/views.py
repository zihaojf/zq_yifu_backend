from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from .serializers import (
    CustomPasswordLoginSerializer,
    PasswordLoginSerializer,
    SmsMsgSerializer,
    ZqAuthLoginSerializer,
)


class PasswordLoginView(TokenObtainPairView):
    serializer_class = PasswordLoginSerializer


class CustomPasswordLoginView(TokenObtainPairView):
    """
    自定义账号密码登录
    """

    serializer_class = CustomPasswordLoginSerializer


class ZqAuthLoginView(TokenObtainPairView):
    """
    zq auth 登录视图
    """

    queryset = User.objects.all()
    serializer_class = ZqAuthLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        增加 post 方法, 支持 sso 登录
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            raise ApiException(
                ResponseType.ThirdLoginFailed,
                msg="自强账号登录失败",
                detail="生成token时simple jwt发生TokenError",
                record=True,
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SmsMsgView(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    """
    ## create:
      - code为空: 发送短信验证码
      - code不为空: 验证短信验证码

    测试 从 console 中展示结果
    """

    queryset = None
    serializer_class = SmsMsgSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # 便于 browser api 访问
        # 去掉后无法通过浏览器界面访问 post 接口
        raise ApiException(ResponseType.MethodNotAllowed, msg="不支持GET方法发送短信")
