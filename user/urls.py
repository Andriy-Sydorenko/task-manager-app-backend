from django.urls import path

from user.views import MeView

urlpatterns = [
    path("", MeView.as_view(), name="me"),
]
