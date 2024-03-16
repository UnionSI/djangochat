from django.shortcuts import render
from functools import wraps
from django.contrib.auth.decorators import login_required


def administrador_requirido(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.perfil:
            if request.user.perfil.nombre == 'Administrador':
                return view_func(request, *args, **kwargs)
        return render(request, 'restringido.html')
    return wrapper
