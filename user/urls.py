from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import RegistrationView, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegistrationView.as_view(), name="register"),
]
