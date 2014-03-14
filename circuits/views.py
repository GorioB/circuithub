from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from circuits.models import RawList, CircuitList
from pricing.models import *
import names
#####util
def incIfExisting(owner,rawname,checklistname=''):
	d = RawList.objects.filter(owner=owner,name=rawname)
	if checklistname=='':
		if len(d)==0:
			return rawname
		else:
			return incIfExisting(owner,rawname+"_new")
	else:
		d = d[0]
		d = d.circuitlist_set.filter(name=checklistname)
		if len(d)==0:
			return checklistname
		else:
			return incIfExisting(owner,rawname,checklistname+"_new")
####views
def listRawLists(request,owner_id):
	listowner = request.user.username
	ownersLists = RawList.objects.filter(owner=owner_id)
	context = RequestContext(request,{'listlist':ownersLists})
	return render(request,'circuits/listTemplate.html',context)

def goToHome(request):
	if(request.user.is_authenticated()):
		context = RequestContext(request)
		return redirect("/u/"+request.user.username)
	else:
		return redirect("/u/guest")
		
def printFriendly(request,owner_id,list_id,circuit_name):
	listowner = request.user.username
	rawList = RawList.objects.filter(owner=listowner,name=list_id)[0]
	circuitList = rawList.circuitlist_set.filter(name=circuit_name)[0]
	contents = circuitList.realelement_set.all()
	totalCost=0
	for i in contents:
		totalCost+=float(i.price)*i.device_count

	context = RequestContext(request,{'clist':circuitList})
	return render(request,'circuits/printTemplate.html',context)

def listRawContents(request,owner_id,list_id):
	listowner= request.user.username
	ownersLists=RawList.objects.filter(owner=owner_id,name=list_id)[0]
	contents = ownersLists.rawelement_set.all()
	context = RequestContext(request,{'contents':contents})
	return render(request,'circuits/contentsTemplate.html',context)
	
def listCircuitContents(request,owner_id,list_id,circuit_name):
	listViewer=request.user.username
	rawList = RawList.objects.filter(owner=owner_id,name=list_id)[0]
	circuitList = rawList.circuitlist_set.filter(name=circuit_name)[0]
	contents = circuitList.realelement_set.all()
	totalCost=0
	for i in contents:
		totalCost+=float(i.price)*i.device_count
	context = RequestContext(request,{'contents':contents,'cost':totalCost})
	return render(request,'circuits/checklistTemplate.html',context)

def createChecklist(request,owner_id,list_id):
	user = request.user.username
	circuit_name = request.POST['circuit_name'].replace(' ','_')
	rawList = RawList.objects.filter(owner=owner_id,name=list_id)[0]
	newname=list_id
	if rawList.owner!=user:
		oldRawListContents = rawList.rawelement_set.all()
		rawList.pk=None
		rawList.owner=user
		rawList.save()
		newname = incIfExisting(user,list_id)
		rawList.name=newname
		for i in oldRawListContents:
			rawList.rawelement_set.create(main_value=i.main_value,
				device_type=i.device_type,
				device_subtype=i.device_subtype,
				device_model=i.device_model,
				device_count=i.device_count)

	if(circuit_name!=''):
		rawList.generateCircuitList(incIfExisting(user,newname,circuit_name))
	else:
		rawList.generateCircuitList(incIfExisting(user,newname,names.giveName()))

	return redirect('circuits.views.listRawLists',owner_id=user)

def updateChecklist(request,owner_id,list_id,circuit_name):
	user = request.user.username
	rawList = RawList.objects.filter(owner=owner_id,name=list_id)[0]
	circuitList = rawList.circuitlist_set.filter(name=circuit_name)[0]
	contents = circuitList.realelement_set.all()

	for i in contents:
		if i.bought_count != float(request.POST[str(i.pk)]):
			element = circuitList.realelement_set.filter(pk=i.pk)[0]
			element.bought_count=float(request.POST[str(i.pk)])
			element.save()
		if float(i.price) != float(request.POST[str(i.pk)+"_price"]):
			element = circuitList.realelement_set.filter(pk=i.pk)[0]
			element.price=float(request.POST[str(i.pk)+"_price"])
			element.save()
			incrementPriceOrNewEntry(m_type=element.device_type,s_type=element.device_subtype,mod=element.device_model,pri=element.price)

	return redirect('circuits.views.listCircuitContents',owner_id=owner_id,list_id=list_id,circuit_name=circuit_name)

def deleteRawList(request,owner_id,list_id):
	user=request.user.username
	rawList = RawList.objects.filter(owner=user,name=list_id)[0]
	circuitList = rawList.circuitlist_set.all()
	for i in circuitList:
		i.delete()
		
	rawList.delete()
	return redirect('circuits.views.listRawLists',owner_id=user)

def deleteCheckList(request,owner_id,list_id,circuit_name):
	user = request.user.username
	rawList = RawList.objects.filter(owner=owner_id,name=list_id)[0]
	circuitList = rawList.circuitlist_set.filter(name=circuit_name)[0]
	circuitList.delete()
	return redirect('circuits.views.listRawLists',owner_id=user)

# Create your views here.
