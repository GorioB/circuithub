from django.db import models

# Create your models here.

class PricingEntry(models.Model):
	main_type=models.CharField(max_length=20)
	sub_type=models.CharField(max_length=20)
	model=models.CharField(max_length=20)
	price=models.CharField(max_length=20)
	notes=models.CharField(max_length=80)
	times_used = models.IntegerField()

