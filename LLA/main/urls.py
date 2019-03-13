"""LLA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views
from django.urls import path

app_name = 'main'

#wszystkie odnośniki url; drugi atrybut odnosi się do odpowiedniej funkcji w pliku views i określa, co ma wyświetlać dany odnośnik
urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("register/", views.register, name='register'),
    path("logout/", views.logout_request, name='logout'),
    path("login/", views.login_request, name='login'),
    path("contact/", views.contact, name='contact'),
    path("profile/", views.profile_request, name='profile'),
     path("dictionary/", views.show_dictionary, name='dictionary')
]
