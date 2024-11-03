#Para login
from django.contrib.auth import authenticate, login, logout
#para login del modelo de django
from django.contrib.auth.models import User
#Renderizar 
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
#Mostrar mensajes 
from django.contrib import messages
#renderizar
from django.shortcuts import render
#sesiones del usuario
from django.contrib.sessions.models import Session
#para usar el decorador @login Requiered
from django.contrib.auth.decorators import login_required

from .models import Publicaciones
from .forms import PublicacionesForm

# Create your views here.

def MainPage(request):
    messages.success(request, 'Template Funcionando')
    return render(request, 'templatesApp/main.html')

#Vista para listar publicaciones

def lista_publicaciones(request):
    publicaciones = Publicaciones.objects.all()
    return render(request, 'templatesApp/Lista.html', {'publicaciones': publicaciones})

# Vista para crear una nueva publicacion

def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_publicaciones')  # Redirige después de guardar
    else:
        form = PublicacionesForm()  # Se asegura de que el formulario se cargue en solicitudes GET
    
    # Renderiza el formulario en ambas solicitudes GET y POST
    return render(request, 'templatesApp/Crear.html', {'form': form})
    