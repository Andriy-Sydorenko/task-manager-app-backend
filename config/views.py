from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    @staticmethod
    def get(request):
        return Response({"message": "Hello World!"}, status=status.HTTP_200_OK)
