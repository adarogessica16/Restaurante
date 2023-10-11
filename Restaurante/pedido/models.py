from django.db import models
from registro.models import Usuario
from menu.models import Menu 

class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    precio_total = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    menus = models.ManyToManyField(Menu, through='DetallePedido')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cliente.nombre

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pedido.cliente.nombre


