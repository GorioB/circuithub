from django.shortcuts import render,redirect
from django.template import RequestContext
import SchParser
from circuits.models import RawList
from circuits.names import giveName
import re

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

	if request.user.is_authenticated():
		newRealList=RawList(owner=request.user.username,name=f.name.split('.')[0],author=request.user.username)
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