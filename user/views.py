from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from user.serializers import MeSerializer


# TODO: add validation for user registration
class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(email=self.request.user.email)

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
