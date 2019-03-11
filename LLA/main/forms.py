from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class ContactForm(forms.Form):
	imię = forms.CharField(max_length=100)
	email = forms.EmailField(required=True)
	wiadomość = forms.CharField(widget=forms.Textarea)
