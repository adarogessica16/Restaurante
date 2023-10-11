from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Categoria
from .forms import MenuForm
from .models import Menu


def inicioCategoria(request):
    categorias= Categoria.objects.all()
    return render(request, 'menu/categoria.html', {"categorias": categorias})

def addCategoria(request):
    errores= Categoria.objects.validar(request.POST)
    if len(errores) > 0:
        for key, value in errores.items():
            messages.error(request, value)
        return redirect('/menu/categorias')
    else:

        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        categoria= Categoria.objects.create(nombre=nombre, descripcion=descripcion)
        messages.success(request, "Categoria añadida correctamente")
        return redirect('/menu/categorias')

def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    
    if request.method == 'POST':
        errores = Categoria.objects.validar(request.POST)
        if len(errores) > 0:
            for key, value in errores.items():
                messages.error(request, value)
        else:
            categoria.nombre = request.POST['nombre']
            categoria.descripcion = request.POST['descripcion']
            categoria.save()
            messages.success(request, "Actualizado correctamente")
            return redirect('/menu/categorias')
    
    return render(request, 'menu/editar_categoria.html', {'categoria': categoria})


def eliminar_categoria(request, id):
    
    categoria = Categoria.objects.get(id=id)
    categoria.delete()

    return redirect('/menu/categorias')


def crear_menu(request):
    menus = Menu.objects.all()
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear_menu')
    else:
        form = MenuForm()

    return render(request, 'menu/crear_menu.html', {'form': form, 'menus': menus})

def eliminar_menu(request, id):
    menu = Menu.objects.get(id=id)
    menu.delete()
    messages.success(request, "Menú eliminado correctamente")
    
    return redirect('crear_menu')