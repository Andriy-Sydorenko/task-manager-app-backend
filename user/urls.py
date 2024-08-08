from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import MeViewSet

router = DefaultRouter()
router.register(r"me", MeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
