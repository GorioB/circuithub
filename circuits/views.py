from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from circuits.models import RawList


def listRawLists(request,owner_id):
	listsowner = request.user.username
	ownersLists = RawList.objects.filter(owner=owner_id)
	context = RequestContext(request,{'listlist':ownersLists})
	return render(request,'circuits/listTemplate.html',context)


def listRawContents(request,owner_id,list_id):
	listsowner= request.user.username
	ownersLists=RawList.objects.get(owner=owner_id,name=list_id)
	contents = ownersLists.rawelement_set.all()
	context = RequestContext(request,{'contents':contents})
	return render(request,'circuits/contentsTemplate.html',context)



# Create your views here.
