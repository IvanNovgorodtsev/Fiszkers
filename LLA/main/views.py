from django.shortcuts import render, redirect
from .models import Course
from .models import Word
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, ContactForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail
import csv
# Create your views here.

def homepage(request):
		return render(request = request, template_name="main/home.html", context = {"courses": Course.objects.all}) #UWAGA!
		#Tutaj context przzekazuje za pomocą listy courses wszystkie obiekty Course, które potem zostaną przekazane do home.html (patrz - home.html)

def register(request):
	if request.method == "POST": #po wciśnięciu przycisku submite
		form = NewUserForm(request.POST) #korzystamy z domyślnego formularza rejestracji nowego użytkownika
		if form.is_valid():
			user = form.save() #tworzymy objekt, zapisujemy go w tabeli i jednocześnie przypisujemy do zmiennej user
			username = form.cleaned_data.get('username') #przypisujemy zmiennej username wartość 'username' obiektu
			messages.success(request, f"Zarejestrowano pomyślnie") #wyświetlanie wiadomości; po kropce występuje tag wiadomości, dzięki czemu można rozróżniać ich rodzaje i np. dla różnych wiadomości wyświetlać komunikaty w różnej formie
			login(request,user) #od razu po rejestrecji logujemy naszego użytkownika
			messages.info(request, f"Zalogowano jako: {username}")
			return redirect("main:homepage") #przekierowanie do strony głównej
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")

	form = NewUserForm #do zmiennej form przypisujemy domyślny formularz
	#w uproszczeniu render do danego requesta przypisuje url wraz z kontekstem (w tym wypadku, w register.html form będzie przypisany do zmiennej form
	return render(request, "main/register.html", context = {"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Pomyślnie wylogowano")
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
				messages.info(request, f"Zalogowano jako: {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Błędna nazwa użytkownika lub hasło")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")
	form = AuthenticationForm()
	return render(request, "main/login.html", {"form":form})

def contact(request):
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			 # send email code goes here
			 sender_name = form.cleaned_data['name']
			 sender_email = form.cleaned_data ['email']
			 msg = "{0} sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['msg'])
			 send_mail('New Enquiry', msg, sender_email, ['artur.dylewski.27@gmail.com'])
			 messages.info(request, f"Dziekujemy za wiadomosc")
	else:
		form = ContactForm()

	return render(request, "main/contact.html", {"form":form})

def profile_request(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form= ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f"Zaktualizowano profil.")
			return redirect("main:profile")
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form= ProfileUpdateForm(instance=request.user.profile)
	context = {'u_form': u_form, 'p_form':p_form}

	return render(request,"main/profile.html",context)


def create_dictionary(request):
	with open('main/A.csv') as csvfile:
		reader=csv.DictReader(csvfile,delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			print(row)
			english_word=row['english']
			polish_word=row['polish']
			new_word=Word(english=english_word, polish=polish_word)
			new_word.save()

def show_dictionary(request):
		create_dictionary(request)
		return render(request = request, template_name="main/dictionary.html", context = {"dictionary": Word.objects.all()}) #UWAG
