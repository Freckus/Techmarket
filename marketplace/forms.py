from django import forms
from django.contrib.auth.models import User
from .models import Publicaciones, UserInfo, UserPremium, TipoUsuario, Postulante
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid



class RegisterUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name', 'last_name', 'email',  'password', 'password2']
        exclude=['is_superuser','date_joined','is_staff','is_active','groups', 'user_permissions','last_login']

    #Campos de usuarios 
    username = forms.CharField(label='Usuario',required=True, min_length=4, max_length=60,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre de Usuario'}))

    first_name = forms.CharField(label='Nombres',required=True, min_length=4, max_length=60,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre'}))   

    last_name = forms.CharField(label='Apellidos',required=True, min_length=4, max_length=60,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellidos' }))

    email = forms.EmailField(label='Correo Electrónico',required=True,
                                widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'ejemplo@empresa.cl'}))
    
    Telefono=forms.CharField(label='Telefono',max_length=12, 
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Numwero de celular'}))

    password = forms.CharField(label='Contraseña',required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Contraseña'}))

    password2 = forms.CharField(label='Repetir Constraseña',required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Repetir Contraseña'}))

    DateBirth=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),label='Fecha Nacimiento')

    ProfileImage =forms.ImageField(label='Imagen de perfil a Subir',required=False)
    DescripcionUser = forms.CharField( widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label="DescripcionUser",required=False)
    
    #Validar el nombre de usuario
    def clean_Username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        return username

    #Validar Email
    def clean_Email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email

    #Validar telefono
    def clean_Telefono(self):
        Telefono=self.cleaned_data.get('Telefono')
        Telefono = ''.join(filter(str.isdigit, Telefono))
        if len(Telefono)<9:
            raise forms.ValidationError('Ingrese un numero y codigo de pais')
        return Telefono
    
    #Password
    def clean_Password(self):
        cleaned_data=super().clean()
        if cleaned_data.get('password2')!= cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')
    
    #Validar Fecha Nacimiento
    def clean_DateBirth(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('DateBirth')
        if birth_date is None:
            raise forms.ValidationError("La fecha de nacimiento es obligatoria")
        today = timezone.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age <18:
            raise forms.ValidationError("La fecha de nacimiento es obligatoria")
        return birth_date
    
    #Validar imagen perfil
    def clean_ImagenCarnet(self):
        Img=self.cleaned_data.get('ProfileImage')
        return Img

    def clean_DescripcionUser(self):
        DescripcionUser=self.cleaned_data.get('DescripcionUser')
        return DescripcionUser


    #save para modelo usario
    def SaveModelUser(self):
        user= User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),)

        TipeUser = TipoUsuario.objects.get(IdTipeUser=1)
        random_name = str(uuid.uuid4())[:8]

        datauser=UserInfo.objects.create(
            IdInfoUser=str(uuid.uuid4())[:6],
            Telefono=self.cleaned_data.get('Telefono'),
            DateBirth=self.cleaned_data.get('DateBirth'),
            TypeUser=TipeUser,
            DescripcionUser=self.cleaned_data.get('DescripcionUser'),
            ProfileImage=self.cleaned_data.get('ProfileImage'),
            ConfirmedUser=True,
            IdUser=user
            
        )
        return user

    def save(self, commit=True):
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data['password'])  
        if commit:
            user.save()  
        return user

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['Titulo', 'Descripcion', 'ImagePost']



class PostulacionPostForm(forms.ModelForm):
    class Meta:
        model = Postulante
        fields = ['publicacion','usuario']






