from django.http import HttpResponseForbidden



class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from customer.models import IPAddress
        ip = self.getClientIPAddress(request)

        blocked = IPAddress.objects.filter(ip=ip, is_blocked=True)
        if blocked.exists():
            return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Your IP is blocked.</p>")
        response = self.get_response(request)
        return response

    def getClientIPAddress(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')