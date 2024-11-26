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
    Descripcion=models.CharField(max_length=50, default="")
    
 
class Areas (models.Model):
    IdArea=models.AutoField(primary_key=True)
    NombreArea=models.CharField(max_length=50, default= "")
    Descripcion=models.CharField(max_length=50, default= "")
    
class Tecnologias(models.Model):
    IdTecnologias=models.AutoField(primary_key=True)
    NombreTecnologias=models.CharField(max_length=50, default= "")    
    #Fk
    AreaTecnologia=models.ForeignKey(Areas, null=True, blank=True, on_delete=models.RESTRICT)
    

class UsuarioTecnologias(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologias, related_name="usuarios")
    

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
    

class Postulante(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE, related_name='postulantes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
    FechaPostulacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('publicacion', 'usuario')  



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
    