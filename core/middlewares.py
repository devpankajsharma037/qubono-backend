from django.http import JsonResponse
import os

ALLOWED_ORIGINS = [os.getenv('WEB_APP_URL')]

class RestrictBrowserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        return self.get_response(request)
    
        origin = request.headers.get("Origin")
        referer = request.headers.get("Referer")

        if not origin and not referer:
            return JsonResponse({"message": "Access denied!"}, status=403)

        if origin and origin not in ALLOWED_ORIGINS:
            return JsonResponse({"message": "Access denied!"}, status=403)

        return self.get_response(request)
