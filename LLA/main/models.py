from django.db import models
from datetime import datetime
# Create your models here.

#tworzymy tu szablony klas, które będzie wykorzystywać nasza strona; można tu dodać kolejne klasy odnośnie kategorii kursów, następnie łączyć je w jakieś zestawy itd

class Course(models.Model):
	course_title = models.CharField(max_length=200)
	course_description = models.TextField()
	course_published = models.DateTimeField("date published", default = datetime.now())

	def __str__(self):
		return self.course_title