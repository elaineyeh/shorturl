from django.http import HttpResponse
from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class HealthCheckMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.method == "GET" and request.path == "/healthz":
            return HttpResponse("200", status=200)

        response = self.get_response(request)

        return response
