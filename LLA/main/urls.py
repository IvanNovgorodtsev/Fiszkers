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
from .views import  CourseListView, CourseDetailView
app_name = 'main'

#wszystkie odnośniki url; drugi atrybut odnosi się do odpowiedniej funkcji w pliku views i określa, co ma wyświetlać dany odnośnik
urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("register/", views.register, name='register'),
    path("logout/", views.logout_request, name='logout'),
    path("login/", views.login_request, name='login'),
    path("contact/", views.contact, name='contact'),
    path("profile/", views.profile_request, name='profile'),
    path("eng_pol_dictionary/", views.show_dictionary, name='eng_pol_dictionary'),
    # path("dictionary2/", views.create_polish_dictionary, name='dictionary2'),
    path("pol_eng_dictionary/", views.show_polish_dictionary, name='pol_eng_dictionary'),
    path("user_page/", views.user_page, name='user_page'),
    path('course/<pk>/', views.course,name='course'),
    path("mycourse/", views.mycourse, name='mycourse'),
    path("course_creator/", views.course_creator, name='course_creator'),
    path("word_list/", views.word_list, name='word_list')
]
