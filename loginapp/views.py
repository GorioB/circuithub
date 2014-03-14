from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User

def username_exists(username):
	if User.objects.filter(username=username).count():
		return True

	return False

def index_view(request):
	if not request.user.is_authenticated():
		context = RequestContext(request,{})
		return render(request,'login/login_block.html',context)
	else:
		context = RequestContext(request,{'username':request.user.username})
		return render(request,'login/logout_block.html',context)

def login_view(request):
	
	issues = []
	username = request.POST['username']
	password = request.POST['passwd']
	user = authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			return HttpResponseRedirect("/u/"+username[:20])
		else:
			return HttpResponseRedirect("/")
	else:
		
		issues.append("Incorrect username or password :(")
		context = RequestContext(request, {'issues' : issues})
		#return HttpResponseRedirect("/")
		print "theres an error in login"
		return render(request, 'login/login_error.html', context)
		
def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")

def register(request):
	return render (request,'login/register.html')

def register_submit(request):
	issues = []
	username = request.POST['username']
	password = request.POST['password']
	email  = request.POST['email']
	password2 = request.POST['passwordconfirm']

	if username_exists(username):
		print "username already taken"
		issues.append("Username already taken")

	if password!=password2:
		issues.append("Passwords don't match")

	if len(issues):
		print "rendering registerfailure.html"
		context = RequestContext(request,{'issues':issues})
		return render(request,'login/registerfailure.html',context)

	else:
		user = User.objects.create_user(username,email,password)
		user.save()
		user = authenticate(username=username,password=password)
		login(request,user)
		return render(request,'login/registersuccess.html')




# Create your views here.
