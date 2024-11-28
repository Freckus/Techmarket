from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator
from .forms import RegisterUserForm
from .forms import PublicacionForm
from .models import Publicaciones
from .models import UserInfo
from django.contrib.sessions.models import Session 
from django.views import View
from django.utils import timezone
import uuid


def MainPage(request):
    #messages.success(request, 'Template Funcionando')
    return render(request, 'templatesApp/Main.html')

def HomePage(request):
    #messages.succes(request, 'Template Funcionando')
    return render(request, 'templatesApp/Home.html')
####################################################################################################
###Registro de usuario#####

def RegistroTipoUsuario(request):
    return render(request, 'templatesApp/RegisterUserType.html')

def Postdetails(request, IdPublicacion):
    Publicacion = Publicaciones.objects.get(IdPublicacion=IdPublicacion)
    data = {'Publicacion': Publicacion}
    return render(request, 'templatesApp/PostDetails.html', data)


def RegisterUser(request):
    form=RegisterUserForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        user = form.SaveModelUser()
        if user:
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('/login/')
    print("Funciona!")
    return render(request, 'templatesApp/Register.html', {'form': form})
####################################################################################################
@login_required  
def ProfileUser(request):
    profile = UserInfo.objects.get(IdUser=request.user)
    publicaciones = Publicaciones.objects.filter(UsuarioCreador=request.user)
    data = {
        'UserInfo': [profile],
        'Publicaciones': publicaciones  
    }
    return render(request, 'templatesApp/Perfil.html', data)
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
        return redirect('/home')
    else:
        if username1 is None and password1 is None:
            pass
        else:
            messages.error(request, 'Usuario o Contraseña incorrectos')
            return redirect('/login/')
    return render(request, 'templatesApp/Login.html')

@login_required
def CerrarSesion(request):
    print("Sesion Cerrada")
    logout(request)
    messages.success(request,'Sesión finalizada correctamente')
    return redirect('/main/')
####################################################################################################
def main(request):
    messages.success(request, 'Login completado')
    return render(request, 'templatesApp/Main.html')

####################################################################################################
##############################Publicaciones
@method_decorator(login_required, name='dispatch')
class CrearPublicacionView(View):
    def get(self, request):
        form = PublicacionForm()
        return render(request, 'templatesApp/Crear.html', {'form': form})
    
    def post(self, request):
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.UsuarioCreador = request.user
            publicacion.save()
            messages.success(request, 'Publicación Creada Exitosamente')
            return redirect('lista_publicaciones')
        return render(request, 'templatesApp/Crear.html', {'form': form})


#class RegistroUsuario(View):
#    def get(self , request):
#        form= RegisterUser()
#        return render(request, 'templatesApp/Register.html')
#    
#    def post(self, request):
#        form=RegisterUser(request.POST, request.files)
        

class ListaPublicacionesView(View):
    def get(self, request):
        publicaciones = Publicaciones.objects.all()
        return render(request, 'templatesApp/Lista.html', {'publicaciones': publicaciones})

def ListarFreelancers(request):
    Usuarios = User.objects.all()  
    info= UserInfo.objects.all()  
    return render(request, 'templatesApp/Listafreelancers.html', {'Usuarios': Usuarios ,'info':info })
