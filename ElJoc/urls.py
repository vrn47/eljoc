"""
URL configuration for ElJoc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from players_test import views0
from players_db import views
from game import views1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('playerinfo/', views.index, name = 'index'),
    path('playerinfo/<int:pid>/', views.playerinfo, name = 'playerinfo'),
    path('items/', views1.items, name = 'items'),
    path('forecasts/', views1.forecasts, name = 'forecasts'),
    path('standings/', views1.standings, name = 'standings'),
    path('footballdata/', views1.footballdata, name = 'footballdata'),
    path('game/', views1.game, name = 'game'),
    path('oldforecasts/', views1.oldforecasts, name = 'oldforecasts'),
    path('pointstable/', views1.pointstable, name = 'pointstable'),
    path('casa/', views0.casa, name = 'casa')

]
