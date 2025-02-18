from django.urls import include, path
from notifications.views import NotificationsViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter

router = ExtendedSimpleRouter()
router.register(
    prefix="", viewset=NotificationsViewSet, basename="notifications"
)
urlpatterns = [
    path("", include(router.urls)),
]
