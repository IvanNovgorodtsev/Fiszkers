from django.contrib import admin
from .models import Course
from .models import Profile

admin.site.register(Profile)
admin.site.register(Course)