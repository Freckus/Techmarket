from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from marketplace import views
from marketplace.views import RegisterUser,main,MainPage, CerrarSesion, ProfileUser,ListarFreelancers,RegistroTipoUsuario,Postdetails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPage),
    path('home', views.HomePage),
    path('register/', RegistroTipoUsuario),
    path('signup/',RegisterUser),
    path('login/',views.Login),
    path('main/',views.main ),
    path('profile/',views.ProfileUser),
    path('main/',views.CerrarSesion ),
    path('publicaciones/', views.ListaPublicacionesView.as_view(), name='lista_publicaciones'),
    path('ListarFreelancers/', views.ListarFreelancers),
    path('publicaciones/nueva/', views.CrearPublicacionView.as_view(), name='crear_publicacion'),
    ##
    path('post/Details/<str:IdPublicacion>/', views.Postdetails, name='post_details'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#comentario prueba
#imagen