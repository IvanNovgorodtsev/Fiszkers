from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Course
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
# Create your views here.

def homepage(request):
		return render(request = request, template_name="main/home.html", context = {"courses": Course.objects.all})

def register(request):
	if request.method == "POST": #po wciśnięciu przycisku submite
		form = NewUserForm(request.POST) #korzystamy z domyślnego formularza rejestracji nowego użytkownika
		if form.is_valid():
			user = form.save() #tworzymy objekt, zapisujemy go w tabeli i jednocześnie przypisujemy do zmiennej user
			username = form.cleaned_data.get('username') #przypisujemy zmiennej username wartość 'username' obiektu
			messages.success(request, f"Succesfully registred") #wyświetlanie wiadomości; po kropce występuje tag wiadomości, dzięki czemu można rozróżniać ich rodzaje i np. dla różnych wiadomości wyświetlać komunikaty w różnej formie
			login(request,user) #od razu po rejestrecji logujemy naszego użytkownika
			messages.info(request, f"You are now login as: {username}")
			return redirect("main:homepage") #przekierowanie do strony głównej
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")

	form = NewUserForm #do zmiennej form przypisujemy domyślny formularz
	#w uproszczeniu render do danego requesta przypisuje url wraz z kontekstem (w tym wypadku, w register.html form będzie przypisany do zmiennej form
	return render(request, "main/register.html", context = {"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully")
	return redirect("main:homepage")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data = request.POST) #domyślne uwierzytelnianie
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request,user)
				messages.info(request, f"You are now logged in as: {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")
	form = AuthenticationForm()
	return render(request, "main/login.html", {"form":form})
