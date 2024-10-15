from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

router = DefaultRouter()

router.register("api/v1/orders", OrderViewSet)
