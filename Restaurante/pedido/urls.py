from django.urls import path
from . import views


urlpatterns = [
    path('menu_disponible/', views.menu_disponible, name='menus'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('lista/', views.lista, name="mis_pedidos"),
    path('listatotal/', views.listatotal),
    path('eliminar_pedido/<int:id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('confirmar_pedido/<int:pedido_id>/', views.confirmar_pedido, name='confirmar_pedido'),
]