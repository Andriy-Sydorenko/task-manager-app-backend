from django.http import JsonResponse


class CloseUrlWithSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.method)
        if request.method == "POST" and not request.path.endswith("/"):
            return JsonResponse({"error": "ЗАКРИВАЙ СЛЕШ НА ПОСТ ПІДАРАС"}, status=400)
        response = self.get_response(request)
        return response
