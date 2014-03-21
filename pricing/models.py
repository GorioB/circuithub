from django.db import models

# Create your models here.
def incrementPriceOrNewEntry(pri,m_type='',s_type='',mod=''):
	print pri, m_type, s_type, mod
	d = PricingEntry.objects.all()
	if m_type!='':
		d = d.filter(main_type=m_type)
	if s_type!='':
		d = d.filter(sub_type=s_type)
	if mod!='':
		d = d.filter(model=mod)

	d = d.filter(price=str(pri))
	if len(d):
		if d[0].times_used<100:
			d[0].times_used=d[0].times_used+1
			d[0].save()
	else:
		d = PricingEntry(main_type=m_type,sub_type=s_type,model=mod,price=pri,times_used=1,element_identifier=m_type+s_type+mod)
		d.save()

class PricingEntry(models.Model):
	main_type=models.CharField(max_length=20)
	sub_type=models.CharField(max_length=20)
	model=models.CharField(max_length=20)
	price=models.CharField(max_length=20)
	notes=models.CharField(max_length=80)
	times_used = models.IntegerField()
	element_identifier=models.CharField(max_length=20)