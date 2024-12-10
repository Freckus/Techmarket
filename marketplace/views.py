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
from .models import Postulante, AcuerdoPublicacion
from django.contrib.sessions.models import Session 
from django.views import View
from django.utils import timezone
import uuid
from django.http import HttpResponseForbidden


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
    acuerdopublicaciones = AcuerdoPublicacion.objects.filter(Postulante__usuario=request.user).distinct()
    
    data = {
        'UserInfo': [profile],
        'Publicaciones': publicaciones,
        'Postulante': postulaciones,
        'AcuerdoPublicacion': acuerdopublicaciones
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

@method_decorator(login_required, name='dispatch') 
class ElegirPostulante(View):
    def get(self, request, IdPostulantes):
        try:
            # Verificar que el usuario sea el propietario de la publicación
            publicacion = Publicaciones.objects.get(IdPublicacion=IdPostulantes)
            if publicacion.UsuarioCreador != request.user:  # Cambia "usuario" por el campo que relaciona la publicación con su dueño
                logout(request)
                messages.error(request, 'Aceeso denegado. Por favor, inicia sesión nuevamente.')
                return redirect('/login')

            postulaciones = Postulante.objects.filter(publicacion=IdPostulantes)
            usuarios_ids = postulaciones.values_list('usuario_id', flat=True)
            userinfo = UserInfo.objects.filter(IdUser__in=usuarios_ids)

            form = Acuerdo()
            data = {
                'postulaciones': postulaciones,
                'publicacion': publicacion,
                'userinfo': userinfo,
                'form': form,
            }
            return render(request, 'templatesApp/SeleccionarPostulante.html', data)

        except Publicaciones.DoesNotExist:
            return HttpResponseForbidden("Publicación no encontrada o no tienes acceso.")

    def post(self, request, IdPostulantes):
        try:
            # Verificar que el usuario sea el propietario de la publicación
            publicacion = Publicaciones.objects.get(IdPublicacion=IdPostulantes)
            if publicacion.UsuarioCreador != request.user:  # Cambia "usuario" por el campo que relaciona la publicación con su dueño
                return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

            form = Acuerdo(request.POST, request.FILES)
            if form.is_valid():
                # Obtener el postulante seleccionado
                postulante_seleccionado_id = request.POST.get('Postulante')
                postulante_seleccionado = Postulante.objects.get(id=postulante_seleccionado_id)

                # Guardar todos los acuerdos y asignar estado según corresponda
                postulaciones = Postulante.objects.filter(publicacion=IdPostulantes)
                for postulante in postulaciones:
                    acuerdo = form.save(commit=False)  # No guardar aún, para modificar el estado
                    acuerdo.Postulante = postulante  # Asignamos el postulante actual al acuerdo

                    # Asignamos el estado
                    if postulante == postulante_seleccionado:
                        acuerdo.EstadoAcuerdo = 'aprobado'  # Marcamos como aprobado al seleccionado
                    else:
                        acuerdo.EstadoAcuerdo = 'rechazado'  # Los demás como rechazados

                    acuerdo.save()  # Guardamos el acuerdo con el estado correcto

                return redirect('/home')

            return render(request, 'templatesApp/SeleccionarPostulante.html', {'form': form})

        except Publicaciones.DoesNotExist:
            return HttpResponseForbidden("Publicación no encontrada o no tienes acceso.")



def pruebaform(request):
    form = Acuerdo2(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():  
        form.save()  
        return redirect('/home')
    return render(request, 'templatesApp/formprueba.html', {'form': form})

    #=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], default="Pendiente")