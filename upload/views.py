from django.shortcuts import render,redirect
from django.template import RequestContext
import SchParser
from circuits.models import RawList
from circuits.names import giveName

# Create your views here.

def upload(request):
	context = RequestContext(request)
	return render(request,'upload/form.html')

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
	f = request.FILES['upfile']
	e = f.read(f.size)
	b = SchParser.schParts(e)[1]
	if f.name.split('.')[1]!="sch" and f.name.split('.')[1]!="cir":
		return redirect('upload.views.upload')

	if request.user.is_authenticated():
		newRealList=RawList(owner=request.user.username,name=f.name.split('.')[0])
	else:
		newname = giveName()[:20]
		newRealList=RawList(owner="guest",name=newname)

	newRealList.save()
	for i in b:
		newRealList.rawelement_set.create(main_value=i.value,device_type=i.type,device_subtype=i.subtype,device_model=i.model,device_count=i.amount)

	if request.user.is_authenticated():
		return redirect("/u/"+request.user.username)
	else:
		newname2=giveName()[:20]
		newRealList.generateCircuitList(newname2)
		return redirect("/u/guest/"+newname+"/"+newname2)