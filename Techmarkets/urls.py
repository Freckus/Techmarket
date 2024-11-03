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
    path('main/',views.main )
]

