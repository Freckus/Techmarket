from django import forms
#Carga el Modelo de contrib.auth
from django.contrib.auth.models import User
from .models import Publicaciones
from django.core.exceptions import ValidationError
####Ivan  
##############################################################################################################################
############################################################################################################################## 
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model=User
    #Campos que quieres ver 
        fields=['first_name', 'last_name', 'username', 'email', 'password', 'password2']
    #Campos de usuarios 
    first_name = forms.CharField(label='Nombres',required=True, min_length=4, max_length=60,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre'}))   

    last_name = forms.CharField(label='Apellidos',required=True, min_length=4, max_length=60,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellidos' }))

    username = forms.CharField(label='Usuario',required=True, min_length=4, max_length=60,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre de Usuario'}))
    
    email = forms.EmailField(label='Correo Electrónico',required=True,
                                widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'ejemplo@empresa.cl'}))
    
    password = forms.CharField(label='Contraseña',required=True,
                              widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Contraseña'}))

    password2 = forms.CharField(label='Repetir Constraseña',required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Repetir Contraseña'}))
    
    #Validar el nombre de usuario
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        return username

    #Validar el MAIL de usuario EVITAR que no hay dos iguales
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email

    def clean(self):
        cleaned_data=super().clean()
        if cleaned_data.get('password2')!= cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')
    
    #no tomes en cuenta esto es para el modelo del userinfo, me falta agregar los otros metodos
    #def GuardarUsuario(self):
    #    user= User.objects.create_user(
    #        self.cleaned_data.get('username'),
    #        self.cleaned_data.get('email'),
    #        self.cleaned_data.get('password'),
    #        first_name=self.cleaned_data.get('first_name'),
    #        last_name=self.cleaned_data.get('last_name'),)

    def save(self, commit=True):
        user = super().save(commit=False)  # No guarda el usuario aún
        user.set_password(self.cleaned_data['password'])  # Establece la contraseña de forma segura
        if commit:
            user.save()  # Guarda el usuario en la base de datos
        return user
##############################################################################################################################
############################################################################################################################## 
#########BrunoPublicaciones###################################################################################################
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['Titulo', 'Descripcion', 'ImagePost']