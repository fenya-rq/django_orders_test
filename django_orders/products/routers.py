from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import ProductViewSet

router = SimpleRouter()

router.routes.pop()
router.routes.pop()

router.register("api/v1/products", ProductViewSet)
