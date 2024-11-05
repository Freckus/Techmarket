from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from marketplace import views
from marketplace.views import RegisterUser,main,MainPage, CerrarSesion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPage),
    path('register/', RegisterUser),
    path('login/',views.Login),
    path('main/',views.main ),
    path('main/',views.CerrarSesion ),
    path('publicaciones/', views.ListaPublicacionesView.as_view(), name='lista_publicaciones'),
    path('publicaciones/nueva/', views.CrearPublicacionView.as_view(), name='crear_publicacion')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#comentario prueba