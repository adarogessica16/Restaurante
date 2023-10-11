from django.urls import path
from . import views


urlpatterns = [
    path('categorias/', views.inicioCategoria),
    path('process_add_categoria/', views.addCategoria),
    path('eliminar_categoria/<int:id>', views.eliminar_categoria),
    path('editar_categoria/<int:id>/', views.editar_categoria),
    path('crear_menu/', views.crear_menu, name='crear_menu'),
    path('eliminar/<int:id>/', views.eliminar_menu),
]