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

# Create your views here.

def MainPage(request):
    messages.success(request, 'Template Funcionando')
    return render(request, 'templatesApp/main.html')

