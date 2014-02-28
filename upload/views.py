from django.shortcuts import render
from django.template import RequestContext
# Create your views here.
def upload(request):
	context = RequestContext(request)
	return render(request,'upload/form.html')

def viewFile(request):
	f = request.FILES['upfile']
	context = {'contents':f.read(f.size)}
	context = RequestContext(request,context)
	return render(request,'upload/view.html',context)