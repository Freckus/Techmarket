from django.db import models
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
    ProfileImage=models.ImageField(upload_to="media/UserProfile", blank=True, default='media/Userprofile/profile_base.jpg')
    #FK DEL MODelo de usuario django
    IdUser=models.ForeignKey(User,null=True,blank=False, on_delete=models.RESTRICT)##User
    #Fk Modelo propio
    TypeUser=models.ForeignKey(TipoUsuario, null=True,blank=False, on_delete=models.RESTRICT)
    EstadoPremium=models.ForeignKey(UserPremium, null=True, blank=False, on_delete=models.RESTRICT)

class EstadoPost(models.Model):
    IdEstado=models.CharField(primary_key=True, max_length=10)
    NombreEstado=models.CharField(max_length=10)

class Publicaciones (models.Model):
    IdPublicacion:models.CharField(primary_key=True,max_length=10)
    #Guardar el post como un xml o json y generearlo con el template?
    PathPost=models.FileField(upload_to='media/Post', blank=True)
    FechaCreacion=models.DateTimeField(default=0)
    Modificado=models.BooleanField(default=False)
    FechaModificacion=models.DateTimeField(default=0)
    #FK
    UsuarioCreador=models.ForeignKey(User,null=True, blank=False,on_delete=models.RESTRICT)
    EstadoPublicacion=models.ForeignKey(EstadoPost, null=True, blank=False, on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.IdPublicacion

class PublicacionesVisistas (models.Model):
    IdPublicacionesVisita=models.CharField(primary_key=True,max_length=10)
    FechaVisita=models.DateField(default=0)
    #FK
    UserVisita=models.ForeignKey(User,null=True, blank=False, on_delete=models.RESTRICT,  related_name='visitas_user')
    PublicacionVisita=models.ForeignKey(User,null=True, blank=False, on_delete=models.RESTRICT, related_name='visitas_publicacion')

class Chats(models.Model):
    IdChats=models.CharField(primary_key=True, max_length=10)
    ChatsField=models.FileField(upload_to='media/Chats',null=True)
    FechaEnvio=models.DateTimeField(default=0)
    FechaVisto=models.DateTimeField(default=0)
    Visto=models.BooleanField(default=False)
    #FK
    UsuarioEmisor=models.ForeignKey(User, null=True, blank=False, on_delete= models.RESTRICT, related_name='Emisor')
    UsuarioRecetor=models.ForeignKey(User, null=True, blank=False, on_delete= models.RESTRICT, related_name='Receptor')
    Publicaciones=models.ForeignKey(Publicaciones, null=True,blank=False, on_delete=models.RESTRICT)
    