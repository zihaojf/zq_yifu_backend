# from sys import prefix

from django.urls import include, path
from rest_framework_extensions.routers import ExtendedSimpleRouter
from users.views import UserViewSet

router = ExtendedSimpleRouter()

router.register(prefix="", viewset=UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

# urlpatterns += router.urls
