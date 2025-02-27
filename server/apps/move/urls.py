from django.urls import include, path
from move.views import MoveRecordViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter

router = ExtendedSimpleRouter()
router.register(prefix="", viewset=MoveRecordViewSet, basename="move_record")
urlpatterns = [
    path("", include(router.urls)),
]
