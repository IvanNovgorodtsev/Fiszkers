from django.contrib import admin
from .models import Course
from .models import Profile
from .models import Word, Word_POL, FlashCard, CustomWord



admin.site.site_header = 'Languages Learning App Admin'
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Word)
admin.site.register(Word_POL)
admin.site.register(FlashCard)
admin.site.register(CustomWord)


