from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator
from .forms import RegisterUserForm
from .forms import PublicacionForm
from .forms import PostulacionPostForm
from .forms import Acuerdo,Acuerdo2
from .models import Publicaciones
from .models import UserInfo
from .models import Postulante
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
    postulaciones=Postulante.objects.filter(usuario=request.user)
    data = {
        'UserInfo': [profile],
        'Publicaciones': publicaciones,
        'Postulante': postulaciones 
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
#class PostulacionPost(View):
#clase view
def PostulacionPost(request):
    form = PostulacionPostForm(request.POST, request.FILES)
    if form.is_valid():
        postulacion = form.save(commit=False)
        postulacion.usuario = request.user
        postulacion.publicacion = Publicaciones.objects.get(IdPublicacion=IdPublicacion)
        postulacion.save()
        messages.success(request, 'Postulacion exitosa')
        return redirect('Profile')
    return render(request, 'templatesApp/pruebapostulacion.html' , {'form': form})


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

class PublicUser(View):
    def get(self,request, IdUser):
        profileDesc = UserInfo.objects.get(IdUser=IdUser)
        profileUser = User.objects.get(id=IdUser) 
        #publicaciones = Publicaciones.objects.filter(UsuarioCreador=request.user)
        data = {
            'profileDesc': profileDesc,
            'profileUser':profileUser,
            #'Publicaciones': publicaciones
            }
        return render(request, 'templatesApp/PerfilPublico.html', data)

class ListaPublicacionesView(View):
    def get(self, request):
        publicaciones = Publicaciones.objects.all()
        return render(request, 'templatesApp/Lista.html', {'publicaciones': publicaciones})

def ListarFreelancers(request):
    Usuarios = User.objects.all()  
    info= UserInfo.objects.all()  
    return render(request, 'templatesApp/Listafreelancers.html', {'Usuarios': Usuarios ,'info':info })


class Postdetails(View):
    # Método GET
    def get(self, request, IdPublicacion):
        # Obtener la publicación
        Publicacion = Publicaciones.objects.get(IdPublicacion=IdPublicacion)
        UserCreador = Publicacion.UsuarioCreador
        User_Info = UserInfo.objects.get(IdUser=UserCreador)
        form = PostulacionPostForm(initial={
            'publicacion': Publicacion, 
            'usuario': request.user       
        })
        
        data = {'Publicacion': Publicacion, 'User': UserCreador, 'UserInfo': User_Info, 'form': form}
        return render(request, 'templatesApp/PostDetails.html', data)

    # Método POST
    def post(self, request, IdPublicacion):
        form = PostulacionPostForm(request.POST, request.FILES)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.usuario = request.user   # Asegurarse de que el usuario se asigna correctamente
            postulacion.publicacion = Publicaciones.objects.get(IdPublicacion=IdPublicacion)
            postulacion.save()
            messages.success(request, 'Postulación exitosa')
            return redirect('/home')
        return render(request, 'templatesApp/PostDetails.html', {'form': form})

#class ElegirPostulante(View):
#    def get(self, request,IdPostulantes):
#        postulaciones = Postulante.objects.filter(publicacion=IdPostulantes)
#        publicacion = Publicaciones.objects.get(IdPublicacion=IdPostulantes) 
#        usuarios_ids = postulaciones.values_list('usuario_id', flat=True)  
#        userinfo = UserInfo.objects.filter(IdUser__in=usuarios_ids)
#        data={ 'postulaciones':postulaciones,'publicacion':publicacion, 'userinfo':userinfo}
#        return render(request, 'templatesApp/SeleccionarPostulante.html', data)
#
#    def post(self, request, IdPostulantes):
#        form=Acuerdo(request.POST, request.FILES)
#        if form.is_valid():
#            
#            form.save() 
#            return redirect('home')
#        return render(request, 'templatesApp/SeleccionarPostulante.html', {'form': form})
#

class ElegirPostulante(View):
    def get(self, request, IdPostulantes):
        postulaciones = Postulante.objects.filter(publicacion=IdPostulantes)
        publicacion = Publicaciones.objects.get(IdPublicacion=IdPostulantes)
        usuarios_ids = postulaciones.values_list('usuario_id', flat=True)
        userinfo = UserInfo.objects.filter(IdUser__in=usuarios_ids)

        # Creamos un formulario con el postulante seleccionado
        form = Acuerdo()
        
        # Añadimos el postulante al formulario, de modo que se envíe en el formulario
        # Asumimos que el postulante se selecciona mediante el boton
        data = {
            'postulaciones': postulaciones,
            'publicacion': publicacion,
            'userinfo': userinfo,
            'form': form,
        }
        return render(request, 'templatesApp/SeleccionarPostulante.html', data)

    def post(self, request, IdPostulantes):
        form = Acuerdo(request.POST, request.FILES)
        if form.is_valid():
            # Aquí se selecciona el postulante al guardar el acuerdo
            form.save()
            return redirect('/home')
        return render(request, 'templatesApp/SeleccionarPostulante.html', {'form': form})

def pruebaform(request):
    form = Acuerdo2(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():  
        form.save()  
        return redirect('/home')
    return render(request, 'templatesApp/formprueba.html', {'form': form})