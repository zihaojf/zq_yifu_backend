from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomPasswordLoginView,
    PasswordLoginView,
    SmsMsgView,
    ZqAuthLoginView,
)

router = routers.SimpleRouter()

router.register("sms", SmsMsgView, basename="sms")

urlpatterns = [
    path(
        "login/zq/",
        ZqAuthLoginView.as_view(),
        name="zq_auth_login",
    ),  # ZqAuth登录
    path(
        "login/password/", PasswordLoginView.as_view(), name="password_login"
    ),  # 密码登录
    path(
        "login/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 刷新token
    path(
        "login/user/",
        CustomPasswordLoginView.as_view(),
        name="custom_password_login",
    ),
]

urlpatterns += router.urls
