from django.shortcuts import render, redirect
from menu.models import Categoria, Menu
from registro.models import Usuario
from .models import Pedido, DetallePedido
from collections import defaultdict
from decimal import Decimal 
from django.contrib import messages

def crear_pedido(request):
    if request.method == 'POST':
        usuario_id = request.POST['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
        
        if usuario.tipo_usuario == 'cliente':
            pedido = Pedido.objects.create(cliente=usuario)
            
            menus_seleccionados = request.POST.getlist('menu_seleccionado')
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
            #Para verificar si el pedido fue creado
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
    usuario= Usuario.objects.all()
    
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
    pedidos = Pedido.objects.filter(cliente=usuario)
    contexto = {
        "usuario": usuario,
        "pedidos": pedidos
    }

    return render(request, 'pedido/pedido.html', contexto)

def listatotal(request):
    menus = Menu.objects.all()
    usuarios= Usuario.objects.all()
    pedidos= Pedido.objects.all()
    
    contexto = {
        "pedidos": pedidos,
        "menus": menus,
        "usuarios": usuarios
    }
    
    return render(request, 'pedido/pedido_restaurante.html', contexto)

def eliminar_pedido(request, id):
        pedido = Pedido.objects.get(id=id)
        # Eliminar los detalles relacionados con el pedido
        pedido.detallepedido_set.all().delete()
        pedido.delete()
        messages.warning(request, "El pedido fue eliminado.")
        return redirect('/pedido/lista') 