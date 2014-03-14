from django.db import models

# Create your models here.

class pricingEntry(models.Model):
	main_type=CharField(max_length=20)
	sub_type=CharField(max_length=20)
	model=CharField(max_length=20)
	price=CharField(max_length=20)
	notes=CharField(max_length=80)

