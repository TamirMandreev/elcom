from django.db import router
from rest_framework.routers import DefaultRouter

from .views import FactoryViewSet

router = DefaultRouter()

router.register(r'factories', FactoryViewSet, basename='factories')

urlpatterns = router.urls