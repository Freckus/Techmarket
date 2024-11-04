from django.conf import settings
from django.contrib import admin
from django.urls import path
from marketplace import views
from marketplace.views import MainPage
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from marketplace.views import RegisterUser
from marketplace.views import main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPage),
    path('register/', RegisterUser),
    path('login/',views.Login),
    path('main/',views.main ),
    path('publicaciones/', views.ListaPublicacionesView.as_view(), name='lista_publicaciones'),
    path('publicaciones/nueva/', views.CrearPublicacionView.as_view(), name='crear_publicacion')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#comentario prueba