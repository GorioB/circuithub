from django.db import models

# Create your models here.
class RawList(models.Model):
	owner=models.CharField(max_length=20)
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.owner+" "+self.name

class CircuitList(models.Model):
	owner=models.CharField(max_length=20)
	name=models.CharField(max_length=20)
	rawlist = models.ForeignKey(RawList)

class RawElement(models.Model):
	main_value = models.CharField(max_length=20)
	device_type = models.CharField(max_length=20)
	device_subtype = models.CharField(max_length=20)
	rawlist = models.ForeignKey(RawList)
	device_model = models.CharField(max_length=20)
	device_count = models.IntegerField()

class RealElement(models.Model):
	main_value = models.CharField(max_length=20)
	device_type = models.CharField(max_length=20)
	device_subtype = models.CharField(max_length=20)
	device_model = models.CharField(max_length=20)
	circuitlist = models.ForeignKey(CircuitList)
	device_count = models.IntegerField()
	bought_count = models.IntegerField()

	def __unicode__(self):
		return self.device_type+" "+self.main_value
