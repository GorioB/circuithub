from django.shortcuts import render,redirect
from pricing.models import *
from pricingutil import *
from django.template import RequestContext


# Create your views here.
def index(request):
	context=RequestContext(request)
	return render(request,'pricing/form.html')

def recreate(request):
	f = request.FILES['file']
	e = f.read(f.size)
	context ={}
	d = map(createPriceEntry,e.split("\n")[1:])
	return redirect('pricing.views.view')

def view(request):
	d = PricingEntry.objects.all()
	context = {'entries':d}
	return render(request,'pricing/view.html',context)
