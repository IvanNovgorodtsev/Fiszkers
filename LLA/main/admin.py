from django.contrib import admin
from .models import Course
from .models import Profile
from .models import Word



admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Word)