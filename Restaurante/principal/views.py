
from django.shortcuts import render
from registro.utils.decoradores import login_requerido
from menu.models import Categoria, Menu
@login_requerido
def inicio(request):
    if 'usuario' in request.session:
        tipo_usuario = request.session['usuario'].get('tipo_usuario', None)
        print(tipo_usuario)

        if tipo_usuario == 'cliente':

            platos_principales = Menu.objects.filter(categoria__nombre='Platos Principales')

            contexto= {
                'platos_principales': platos_principales
            }

            return render(request, 'inicioCliente.html', contexto)
        elif tipo_usuario == 'admin':
            categorias= Categoria.objects.all()
            menus=Menu.objects.all()
            platos_principales = Menu.objects.filter(categoria__nombre='Platos Principales')
            contexto = {
                'categorias':categorias,
                'menus':menus,
                'platos_principales': platos_principales
            }
            return render(request, 'inicioAdmin.html', contexto)
    return render(request, 'registro/login.html')

