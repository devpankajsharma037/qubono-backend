from rest_framework.response import Response
from rest_framework import status

def checkAccountStatus():
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            userObj = request.user
            if userObj.is_delete:
                context = dict()
                context['status']   = False
                context['code']     = status.HTTP_403_FORBIDDEN
                context['message']  = "This account has been deactivated. Please contact support for assistance."
                return Response(context, status=status.HTTP_403_FORBIDDEN)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def checkRole():
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            userObj = request.user
            if userObj.role not in ['ADMIN']:
                context = dict()
                context['status']   = False
                context['code']     = status.HTTP_403_FORBIDDEN
                context['message']  = "Access denied!"
                return Response(context, status=status.HTTP_403_FORBIDDEN)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator