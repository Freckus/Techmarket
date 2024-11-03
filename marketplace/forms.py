from django import forms 
from .models import Publicaciones

class PublicacionesForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['PathPost', 'EstadoPublicacion']