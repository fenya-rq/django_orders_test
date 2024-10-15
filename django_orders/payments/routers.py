from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet

router = DefaultRouter()

router.register("api/v1/pay", PaymentViewSet)
