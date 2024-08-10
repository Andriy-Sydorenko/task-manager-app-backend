from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class HelloView(GenericAPIView):
    @staticmethod
    def get(request):
        return Response({"message": "Hello World!"}, status=status.HTTP_200_OK)
