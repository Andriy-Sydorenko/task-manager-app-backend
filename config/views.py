from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.choices import OpenAIEngines
from config.openai_client import client as openai_client


class GetPredictionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        chat_completion = openai_client.chat.completions.create(
            model=OpenAIEngines.GPT_3_5_TURBO,
            messages=[{"role": "user", "content": "Give me a prediction for today"}],
        )
        return Response(chat_completion)
