from rest_framework.routers import DefaultRouter
from .views import FavouriteViewSet

router = DefaultRouter()
router.register(r"", FavouriteViewSet, basename="favorites")

urlpatterns = router.urls
