from django.http import HttpResponse
from django.shortcuts import redirect


def restrict_access_to_groups(groups:list):
    def decorate(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name__in=groups).exists() :
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('you are not authentecated to view this page')
        return wrapper_func
    return decorate
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func