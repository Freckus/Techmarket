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
#MENSAJES
from django.contrib import messages
#sesiones del usuario
from django.contrib.sessions.models import Session
#para usar el decorador @login Requiered
from django.contrib.auth.decorators import login_required
#Carga de los forms
from .forms import RegisterUserForm



def MainPage(request):
    messages.success(request, 'Template Funcionando')
    return render(request, 'templatesApp/Main.html')

####################################################################################################
###Registro de usuario#####
def RegisterUser(request):
    form=RegisterUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
    #ACA AGREGAR EL METODO PARA EL usuario userinfo no tomees essto en cuenta bruno user = form.save()
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('/login/')
#el {'form': form} le pasa el contexto del formulario
    print("Funciona!")
    return render(request, 'templatesApp/Register.html', {'form': form})
####################################################################################################

####################################################################################################
###Iniciar Sesion de usuario#####
def Login(request):
    username1=request.POST.get('username')
    password1=request.POST.get('password')
    log="username:{0} y password:{1}"
    print(log.format(username1, password1))
    user=authenticate(username=username1, password=password1)
    if user:
        login(request, user)
        messages.success(request, 'Bienvenidos {}'.format(user.username))
        request.session['user'] = username1
        request.session['clave'] = password1
        return redirect('/main/')
    else:
        if username1 is None and password1 is None:
            pass
        else:
            messages.error(request, 'Usuario o Contraseña incorrectos')
            return redirect('/login/')
    return render(request, 'templatesApp/Login.html')
####################################################################################################

def main(request):
    messages.success(request, 'Login completado')
    return render(request, 'templatesApp/Main.html')