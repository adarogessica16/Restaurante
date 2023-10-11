from django.contrib import messages
from django.shortcuts import redirect

def login_requerido(function):
    def wrap(request, *args, **kwargs):

        if 'usuario' not in request.session:
            messages.error(request, 'Debes iniciar sesion con tu cuenta!')
            return redirect('/registro/login/')

        return function(request, *args, **kwargs)

    return wrap 