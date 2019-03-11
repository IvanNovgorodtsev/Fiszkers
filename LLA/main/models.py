from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

#tworzymy tu szablony klas, które będzie wykorzystywać nasza strona; można tu dodać kolejne klasy odnośnie kategorii kursów, następnie łączyć je w jakieś zestawy itd

class Profile (models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	image=models.ImageField(default='default.jpg',upload_to='profile_pics')
	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self):
		super().save()
		img = Image.open(self.image.path)

		if img.height > 300 or img.width >300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)


class Course(models.Model):
	course_title = models.CharField(max_length=200)
	course_description = models.TextField()
	course_published = models.DateTimeField("date published", default = datetime.now())

	def __str__(self):
		return self.course_title