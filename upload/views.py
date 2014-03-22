from django.shortcuts import render,redirect
from django.template import RequestContext
import SchParser
from circuits.models import RawList
from circuits.names import giveName
import re
from pricing.models import *

from circuits.views import incIfExisting

from pricing.models import *
from django.core import serializers #for sending json

import json
from django.http import HttpResponse


# Create your views here.

issues = []

def upload(request):
	context = RequestContext(request)
	
	if (len(issues) == 0): #if there's an issue, don't go here
		return render(request,'upload/form.html')
	else:
		print ">>>> theres an issue"
		context = RequestContext(request, {'issues' : issues})
		return render(request, 'upload/upload_error.html', context);
	
	
def viewFile(request):

	f = request.FILES['upfile']
	e = f.read(f.size)
	p,b = SchParser.schParts(e)
	info=''
	for i in range(0,len(b)):
		info=info+"\n"+"name: "+b[i].name+" model= "+b[i].model+" value= "+b[i].value

	context = {'contents':info}
	context = RequestContext(request,context)
	

	return render(request,'upload/view.html',context)

	
def userUpload(request):
	issues[:] = []
	f = request.FILES['upfile']
	e = f.read(f.size)
	
	
	if (re.search("!DOCTYPE eagle SYSTEM", e) == None):
		issues.append('Not a valid EAGLE schematic!')
		print "upload error"
		#context = RequestContext(request, {'issues' : issues})
		return redirect('upload.views.upload')
	
	b = SchParser.schParts(e)[1]
	if f.name.split('.')[1]!="sch" and f.name.split('.')[1]!="cir":
		return redirect('upload.views.upload')

	fname = f.name.split('.')[0]
	fname = ''.join(e for e in fname if e.isalnum())
	if request.user.is_authenticated():
		newRealList=RawList(owner=request.user.username,name=incIfExisting(request.user.username,fname),author=request.user.username)
	else:
		newname = giveName()
		newRealList=RawList(owner="guest",name=newname,author='guest')

	newRealList.save()
	for i in b:
		newRealList.rawelement_set.create(main_value=i.value,device_type=i.type,device_subtype=i.subtype,device_model=i.model,device_count=i.amount)

	if request.user.is_authenticated():
		return redirect("/u/"+request.user.username)
	else:
		newname2=giveName()
		newRealList.generateCircuitList(newname2)
		return redirect("/u/guest/"+newname+"/"+newname2)
		
		
def manual(request):
	return render(request, 'upload/manual.html')
	
def manualUpload(request):
	
	print str(request.POST)
	
	
	temp = request.POST['maxrow']	
	if(temp == u''):
		maxrow = 0;
	else:
		maxrow = int(temp)
	
	newname = giveName()
	if request.user.is_authenticated():
		newRealList=RawList(owner=request.user.username,name=newname,author=request.user.username)
	else:
		newRealList=RawList(owner="guest",name=newname,author='guest')		
	
	newRealList.save()
	
	for i in range (0, maxrow):
		value = parseValue(request, 'c-val-' + str(i+1))
		type = parseValue(request, 'c-type-' + str(i+1))
		subtype = parseValue(request, 'c-subtype-' + str(i+1))
		model = value
		count = parseValue(request, 'c-qty-' + str(i+1))
		
		
		if (type == u'RLC'):
			model = subtype
		if (type == 'BJT'):
			value = ""
		if (type == "Diode"):
			value = ""
		
		try:
			newRealList.rawelement_set.create(main_value=value,device_type=type,device_subtype=subtype,device_model=model,device_count=count)
		except:
			continue



	if request.user.is_authenticated():
		return redirect("/u/"+request.user.username)
	else:
		newname2=giveName()
		newRealList.generateCircuitList(newname2)
		return redirect("/u/guest/"+newname+"/"+newname2)

		
def getPricelist(request):
	response_data = serializers.serialize("json", PricingEntry.objects.all())
	return HttpResponse(json.dumps(response_data), content_type="application/json")
	
def parseValue(request, key):
	print "finding key: " + key
	try:
		temp = request.POST[key]	
	except:
		temp = "";
	
	print "returned " + temp
	return temp


	
