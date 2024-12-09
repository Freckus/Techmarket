from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# crear modelo
class TipoUsuario(models.Model):
    IdTipeUser= models.IntegerField(primary_key=True)
    NamofType= models.CharField(max_length=10)
   
class InfoPago(models.Model):
    IdInfoPago=models.CharField(primary_key=True, max_length=10)
    FechaPago=models.DateTimeField(default=0)
    IdTransaccion=models.CharField(blank=True, max_length=10)

class  UserPremium(models.Model):
    IdUserPremium=models.CharField(primary_key=True,max_length=10)
    FechaPago=models.DateTimeField(null=True, blank=True)
    FechaFin=models.DateField(default=0)
    UserPremium=models.BooleanField(default=False)
    #Fk
    IdPago=models.ForeignKey(InfoPago, null=True,blank=False, on_delete=models.RESTRICT)

class UserInfo(models.Model):
    IdInfoUser=models.CharField(primary_key=True,max_length=10)
    DateBirth = models.DateField(null=True, blank=True)#default 0 por errores
    ConfirmedUser=models.BooleanField(default=False)
    Telefono = models.CharField(max_length=12, default=0)
    ProfileImage=models.ImageField(upload_to="UserProfile", blank=True, default='UserProfile/profile_base.jpg')
    DescripcionUser = models.TextField(max_length=20000, default="")
    Clasificacion=models.DecimalField(max_digits=2,decimal_places=1, default=0)
    #FK DEL MODelo de usuario django
    IdUser=models.ForeignKey(User,null=True,blank=False, on_delete=models.RESTRICT)##User
    #Fk Modelo propio
    TypeUser=models.ForeignKey(TipoUsuario, null=True,blank=True, on_delete=models.RESTRICT)
    EstadoPremium = models.ForeignKey(UserPremium, null=True, blank=True, on_delete=models.RESTRICT)

class EstadoPost(models.Model):
    IdEstado=models.CharField(primary_key=True, max_length=10)
    NombreEstado=models.CharField(max_length=10)

class Publicaciones (models.Model):
    IdPublicacion:models.CharField(primary_key=True,max_length=10)
    #Guardar el post como un xml o json y generearlo con el template?
    Titulo = models.CharField(max_length=500, default=0)
    Descripcion= models.TextField(max_length=5000, default=0)
    ImagePost=models.ImageField(upload_to='images', default='media/resources/favicon.png')
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    Modificado=models.BooleanField(default=False)
    FechaModificacion=models.DateTimeField(auto_now_add=True)
    #FK   
    UsuarioCreador=models.ForeignKey(User,null=True, blank=False,on_delete=models.RESTRICT)
    EstadoPublicacion=models.ForeignKey(EstadoPost, null=True, blank=False, on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.Titulo

class PublicacionesVisistas (models.Model):
    IdPublicacionesVisita=models.CharField(primary_key=True,max_length=10)
    FechaVisita=models.DateField(default=0)
    #FK
    UserVisita=models.ForeignKey(User,null=True, blank=False, on_delete=models.RESTRICT,  related_name='visitas_user')
    PublicacionVisita=models.ForeignKey(User,null=True, blank=False, on_delete=models.RESTRICT, related_name='visitas_publicacion')

class Chats(models.Model):
    IdChats = models.CharField(primary_key=True, max_length=10)
    Mensaje = models.TextField(null=True, blank=True)  # Mensaje de texto
    ArchivoAdjunto = models.FileField(upload_to='media/Chats', null=True, blank=True)  # Soporte para archivos
    FechaEnvio = models.DateTimeField(default=timezone.now)  # Fecha de envío del mensaje
    FechaVisto = models.DateTimeField(null=True, blank=True)  # Fecha en la que se marcó como visto
    Visto = models.BooleanField(default=False)  # Indicador de si el mensaje ha sido leído
    # FK
    UsuarioEmisor = models.ForeignKey(User, null=True, blank=False, on_delete=models.RESTRICT, related_name='Emisor')
    UsuarioReceptor = models.ForeignKey(User, null=True, blank=False, on_delete=models.RESTRICT, related_name='Receptor')
    Publicacion = models.ForeignKey('Publicaciones', null=True, blank=True, on_delete=models.RESTRICT)  # Relación opcional con Publicaciones

class Conversaciones(models.Model):
    IdConversacion = models.CharField(primary_key=True, max_length=10)
    Participantes = models.ManyToManyField(User)  # Usuarios en la conversación
    FechaCreacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversación {self.IdConversacion}"
