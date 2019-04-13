from django.shortcuts import render, redirect
from .models import Course, FlashCard
from .models import Word, Word_POL, Course_signup, CustomWord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, ContactForm, UserUpdateForm, ProfileUpdateForm, CreateCourseForm, AddWordToCourseForm
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView
import pandas as pd
import numpy as np
import re
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
			return redirect("main:user_page") #przekierowanie do strony głównej
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
				return redirect("main:user_page")
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
			 sender_name = form.cleaned_data['imię']
			 sender_email = form.cleaned_data ['email']
			 msg = "{0} sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['wiadomość'])
			 send_mail('New Enquiry', msg, sender_email, ['contact@lla.com'])
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
	file=pd.read_csv("main/A.csv", delimiter=';')
	for i in range(len(file)):
		english_word=file.iloc[i]['english']
		polish_word=file.iloc[i]['polish']
		new_word=Word(english=english_word, polish=polish_word)
		new_word.save()
	return render(request = request, template_name="main/eng_pol_dictionary.html", context = {"eng_pol_dictionary": Word.objects.all()})


def create_polish_dictionary(request):
	file = pd.read_csv('main/pol_eng.csv', sep="\n", header=None)
	words = np.array([])
	for i in range(2):
		line = file[0][i]
		line2 = file[0][i + 1]
		x = re.search("[1-9].", line)
		y = re.search("[1-9].", line2)
		if x == None and y == None:
			words = np.append(words, line)

	pol = words[0:][::2]
	eng = words[1:][::2]

	for i in range(len(pol) - 1):
		w=re.search("\/.*?\/.*[\<.*?\>]?",pol[i])
		y=re.search("\[.*\]",eng[i])
		new_word = Word_POL(polish_w=pol[i].replace(w[0],""), english_w=eng[i].replace(y[0],"")+"\t"+y[0])
		new_word.save()

	return render(request=request, template_name="main/pol_eng_dictionary.html", context={"pol_eng_dictionary": Word_POL.objects.all()})


def show_dictionary(request):
	word_list = Word.objects.all()
	paginator = Paginator(word_list, 25) # Show 25 words per page
	page = request.GET.get('page')
	words = paginator.get_page(page)
	return render(request = request, template_name="main/eng_pol_dictionary.html", context = {"eng_pol_dictionary": words })

def show_polish_dictionary(request):
	word_list = Word_POL.objects.all()
	paginator = Paginator(word_list, 25) 
	page = request.GET.get('page')
	words = paginator.get_page(page)
	return render(request = request, template_name="main/pol_eng_dictionary.html", context = {"pol_eng_dictionary": words})


def user_page(request):
	return render(request,"main/user_page.html", context = {"courses": Course.objects.all})	

def course(request, pk):
	current_user = request.user
	obj = Course.objects.get(pk=pk)
	q=Course_signup.objects.filter(profile=current_user)
	if q.filter(course=obj.id):
		return render(request,"main/course_detail.html")
	else:
		Course_signup(profile=current_user, course=obj).save()
		return render(request, "main/course_detail.html")

def course_request(request):
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

def course_creator(request):
	if request.method == "POST":
		form = CreateCourseForm(request.POST)
		if form.is_valid():
			 form.save()
			 messages.info(request, f"Kurs został utworzony")
	else:
		form = CreateCourseForm()
	return render(request,"main/course_creator.html",  context ={"form":form})

class CourseListView(ListView):
	model = Course
	template_name= 'main/user_page.html'
	context_object_name = 'courses'

class CourseDetailView(DetailView):
	model = Course

def mycourse(request):
	course = int(request.GET.get('course', 1))
	if request.method == "POST" and 'known' in request.POST:
		fid = request.POST.get('fid')
		messages.info(request, f"Brawo!")
		flashcard = FlashCard.objects.get(id=fid)
		flashcard.known = 1
		flashcard.save()
	elif request.method == "POST" and 'unknown' in request.POST:
		messages.info(request, f"Musisz jeszcze poćwiczyć!")
	return render(request, "main/mycourse.html", context = {"flashcards": FlashCard.objects.all(), "course": course})

def word_list(request):
	course = (int)(request.GET.get('course',1))
	if request.method == "POST":
		form = AddWordToCourseForm(request.POST)
		if form.is_valid():
			form.save()
			messages.info(request, f"Słowo zostało dodane")
	else:
		form = AddWordToCourseForm()
	return render(request, "main/word_list.html", context = {"CustomWord": CustomWord.objects.all(), "Course": course, "form":form})

