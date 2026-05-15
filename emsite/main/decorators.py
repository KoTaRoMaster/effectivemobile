from functools import wraps
from django.http import HttpResponse, HttpResponseForbidden


def authenticate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        return view_func(request, *args, **kwargs)

    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden()

        return view_func(request, *args, **kwargs)

    return wrapper



def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        if not request.user.is_superuser:
            return HttpResponseForbidden()

        return view_func(request, *args, **kwargs)

    return wrapper

