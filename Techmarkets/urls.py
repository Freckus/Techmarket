"""
URL configuration for Techmarkets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from marketplace import views
from marketplace.views import MainPage
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPage, name='main_page'),
    path('lista_publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
]

