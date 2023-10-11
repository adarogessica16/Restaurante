# forms.py
from django import forms
from .models import Menu
from .models import Categoria

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nombre', 'precio', 'categoria', 'imagen']

        labels = {
            'nombre': 'Nombre:',
            'precio': 'Precio:',
            'categoria': 'Categoría:',
            'imagen': 'Imagen:',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'categoria': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorias = [(categoria.id, categoria.nombre) for categoria in Categoria.objects.all()]
        self.fields['categoria'].choices = categorias