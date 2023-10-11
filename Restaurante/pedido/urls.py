from django.urls import path
from . import views


urlpatterns = [
    path('menu_disponible/', views.menu_disponible),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('lista/', views.lista),
    path('listatotal/', views.listatotal),
    path('eliminar_pedido/<int:id>/', views.eliminar_pedido, name='eliminar_pedido'),
]