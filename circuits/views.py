from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from circuits.models import RawList, CircuitList
import names

def listRawLists(request,owner_id):
	listowner = request.user.username
	ownersLists = RawList.objects.filter(owner=owner_id)
	context = RequestContext(request,{'listlist':ownersLists})
	return render(request,'circuits/listTemplate.html',context)

def printFriendly(request,owner_id,list_id,circuit_name):
	listowner = request.user.username
	rawList = RawList.objects.get(owner=listowner,name=list_id)
	circuitList = rawList.circuitlist_set.get(name=circuit_name)
	contents = circuitList.realelement_set.all()
	totalCost=0
	for i in contents:
		totalCost+=int(i.price)*i.device_count

	context = RequestContext(request,{'clist':circuitList})
	return render(request,'circuits/printTemplate.html',context)

def listRawContents(request,owner_id,list_id):
	listowner= request.user.username
	ownersLists=RawList.objects.get(owner=owner_id,name=list_id)
	contents = ownersLists.rawelement_set.all()
	context = RequestContext(request,{'contents':contents})
	return render(request,'circuits/contentsTemplate.html',context)
	
def listCircuitContents(request,owner_id,list_id,circuit_name):
	listowner = request.user.username
	rawList = RawList.objects.get(owner=owner_id,name=list_id)
	circuitList = rawList.circuitlist_set.get(name=circuit_name)
	contents = circuitList.realelement_set.all()
	totalCost=0
	for i in contents:
		totalCost+=int(i.price)*i.device_count
	context = RequestContext(request,{'contents':contents,'cost':totalCost})
	return render(request,'circuits/checklistTemplate.html',context)

def createChecklist(request,owner_id,list_id):
	user = request.user.username
	circuit_name = request.POST['circuit_name'].replace(' ','_')
	rawList = RawList.objects.get(owner=user,name=list_id)
	if(circuit_name!=''):
		rawList.generateCircuitList(circuit_name)
	else:
		rawList.generateCircuitList(names.giveName())

	return redirect('circuits.views.listRawLists',owner_id=user)

def updateChecklist(request,owner_id,list_id,circuit_name):
	user = request.user.username
	rawList = RawList.objects.get(owner=owner_id,name=list_id)
	circuitList = rawList.circuitlist_set.get(name=circuit_name)
	contents = circuitList.realelement_set.all()

	for i in contents:
		if i.bought_count != int(request.POST[str(i.pk)]):
			element = circuitList.realelement_set.get(pk=i.pk)
			element.bought_count=int(request.POST[str(i.pk)])
			element.save()
		if i.price != int(request.POST[str(i.pk)+"_price"]):
			element = circuitList.realelement_set.get(pk=i.pk)
			element.price=int(request.POST[str(i.pk)+"_price"])
			element.save()
	return redirect('circuits.views.listCircuitContents',owner_id=owner_id,list_id=list_id,circuit_name=circuit_name)

def deleteRawList(request,owner_id,list_id):
	user=request.user.username
	rawList = RawList.objects.get(owner=owner_id,name=list_id)
	rawList.delete()
	return redirect('circuits.views.listRawLists',owner_id=user)

def deleteCheckList(request,owner_id,list_id,circuit_name):
	user = request.user.username
	rawList = RawList.objects.get(owner=owner_id,name=list_id)
	circuitList = rawList.circuitlist_set.get(name=circuit_name)
	circuitList.delete()
	return redirect('circuits.views.listRawLists',owner_id=user)

# Create your views here.
