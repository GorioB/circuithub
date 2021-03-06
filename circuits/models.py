from django.db import models
from upload.SchParser import findPrice
from pricing.models import *

def findBestPriceMatch(raw):
	pool = PricingEntry.objects.filter(model=raw.device_model.upper())
	if len(pool)==0:
		pool = PricingEntry.objects.filter(main_type=raw.device_type.upper(),sub_type=raw.device_subtype.upper())
	if len(pool)==0:
		return 0
	elif len(pool)==1:
		return pool[0].price
	else:
		return pool.order_by('-times_used')[0].price

# Create your models here.
class RawList(models.Model):
	owner=models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	author=models.CharField(max_length=20)

	def __unicode__(self):
		return self.owner+" - "+self.name

	def generateCircuitList(self,name):
		c = self.circuitlist_set.create(owner=self.owner,name=name)
		for i in self.rawelement_set.all():
			c.realelement_set.create(
				main_value=i.main_value,
				device_type=i.device_type,
				device_subtype=i.device_subtype,
				device_model=i.device_model,
				device_count=i.device_count,
				bought_count=0,
				price=str(findBestPriceMatch(i)))
		return c

#CircuitList owner field is for removal but I forgot why
class CircuitList(models.Model):
	owner=models.CharField(max_length=20)
	name=models.CharField(max_length=20)
	rawlist = models.ForeignKey(RawList)

	#def __unicode__(self):
	#	return self.owner+" - "+str(self.rawlist)+" - "+self.name

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
	price = models.CharField(max_length=20)

	def __unicode__(self):
		return self.device_type+" "+self.main_value
