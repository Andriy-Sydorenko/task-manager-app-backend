from django.http import HttpResponsePermanentRedirect


class CloseUrlWithSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["POST", "PATCH", "PUT", "DELETE"] and not request.path.endswith("/"):
            return HttpResponsePermanentRedirect(request.path + "/")
        response = self.get_response(request)
        return response
