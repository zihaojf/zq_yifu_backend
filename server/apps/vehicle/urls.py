from django.urls import include, path
from rest_framework_extensions.routers import ExtendedSimpleRouter
from vehicle.views import VehicleViewSet

router = ExtendedSimpleRouter()
router.register(prefix="", viewset=VehicleViewSet, basename="vehicle")
urlpatterns = [
    path("", include(router.urls)),
]
