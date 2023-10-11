
from __future__ import unicode_literals
from django.db import models



class CategoriaManager(models.Manager):
    def validar(self, postData):
        errors = {}
        if len(postData['nombre']) < 2:
            errors["nombre"] = "Por favor utiliza un nombre mas largo"
        if len(postData['descripcion']) < 5:
            errors["descripcion"] = "Haz una descripcion mas larga"
        return errors

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= CategoriaManager()


    def __str__(self):
        return self.nombre
    


class Menu(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='menus/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
