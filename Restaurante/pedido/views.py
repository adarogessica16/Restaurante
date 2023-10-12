from django.shortcuts import render, redirect
from menu.models import Categoria, Menu
from registro.models import Usuario
from .models import Pedido, DetallePedido
from collections import defaultdict
from decimal import Decimal 
from django.contrib import messages
from django.core.paginator import Paginator

def crear_pedido(request):
    if request.method == 'POST':
        usuario_id = request.POST['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
        
        if usuario.tipo_usuario == 'cliente':
            menus_seleccionados = request.POST.getlist('menu_seleccionado')
            
            if not menus_seleccionados:
                messages.error(request, "No has seleccionado ningún menú.")
                return redirect('/pedido/menu_disponible')
            
            pedido = Pedido.objects.create(cliente=usuario)
            
            seleccionados_con_cantidad = defaultdict(Decimal)
            
            for menu_id in menus_seleccionados:
                menu = Menu.objects.get(id=menu_id)
                cantidad = Decimal(request.POST.get('cantidad' + menu_id))
                seleccionados_con_cantidad[menu] += cantidad
            
            precio_total_pedido = Decimal('0.0')
            
            for menu, cantidad_total in seleccionados_con_cantidad.items():
                precio = menu.precio
                subtotal = precio * cantidad_total
                precio_total_pedido += subtotal
                
                DetallePedido.objects.create(
                    pedido=pedido,
                    menu=menu,
                    cantidad=cantidad_total,
                    subtotal=subtotal
                )
            
            pedido.precio_total = precio_total_pedido
            pedido.save()
            
            detalles_pedido = DetallePedido.objects.filter(pedido=pedido)
            # Para verificar si el pedido fue creado 
            for detalle in detalles_pedido:
                print(f'Detalle Pedido #{detalle.pedido.id} - Menu: {detalle.menu.nombre}, Cantidad: {detalle.cantidad}, Subtotal: {detalle.subtotal}')
            
            print(f'Se creó el pedido con precio total: {pedido.precio_total}')
            messages.success(request, "El pedido fue agregado exitosamente.")
            return redirect('/pedido/lista')
        else:
            return render(request, {'mensaje': 'No tienes permiso para hacer pedidos.'})

    return redirect('/pedido/menu_disponible')


def menu_disponible(request):
    categorias = Categoria.objects.all()
    menus = Menu.objects.all()
    usuario = Usuario.objects.all()

    # Verificar si se ha enviado un formulario de filtro por categoría
    categoria_filtrada = request.POST.get('categoria')
    if categoria_filtrada:
        # Filtrar los menús por la categoría seleccionada
        menus = Menu.objects.filter(categoria=categoria_filtrada)

    contexto = {
        "categorias": categorias,
        "menus": menus,
        "usuario": usuario
    }
    
    return render(request, 'pedido/menu_disponible.html', contexto)


def lista(request):
    usuario_id = request.session['usuario']['id']
    usuario = Usuario.objects.get(id=usuario_id)
    # Filtrar los pedidos relacionados con el usuario en sesión
    pedidos = Pedido.objects.filter(cliente=usuario).order_by('-created_at')
    contexto = {
        "usuario": usuario,
        "pedidos": pedidos
    }

    return render(request, 'pedido/pedido.html', contexto)

def listatotal(request):
    menus = Menu.objects.all().order_by('-created_at')
    usuarios= Usuario.objects.all()
    pedidos = Pedido.objects.all().order_by('-created_at')
    # Configurar la paginación
    paginator = Paginator(usuarios, 3)
    page = request.GET.get('page') 
    usuarios_pagina = paginator.get_page(page)
    contexto = {
        "pedidos": pedidos,
        "menus": menus,
        "usuarios": usuarios_pagina
    }
    
    return render(request, 'pedido/pedido_restaurante.html', contexto)

def eliminar_pedido(request, id):
        pedido = Pedido.objects.get(id=id)
        # Eliminar los detalles relacionados con el pedido
        pedido.detallepedido_set.all().delete()
        pedido.delete()
        messages.warning(request, "El pedido fue eliminado.")
        return redirect('/pedido/lista') 

def confirmar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pedido.estado = 'confirmado'
    pedido.save()
    messages.success(request, "El pedido fue confirmado al cliente.")
    return redirect('/pedido/listatotal') 