from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Course
from .models import Profile
from .models import Word, FlashCard
#tutaj nadpisujemy 'forms' - dzięki temu możmy do gotowej już klasy UserCreationForm dodać adres email

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email")

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

class ContactForm(forms.Form):
	imię = forms.CharField(max_length=100)
	email = forms.EmailField(required=True)
	wiadomość = forms.CharField(widget=forms.Textarea)

class CreateCourseForm(forms.ModelForm):
	class Meta:
		model=Course
		fields = ['course_title','course_description']

class Check(forms.ModelForm):
	class Meta:
		model = FlashCard
		fields = ('words', 'course', 'known')