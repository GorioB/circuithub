from django.conf.urls import patterns, include, url

urlpatterns = patterns('pricing.views',
	url(r'^$','index'),
	url(r'^recreate/$','recreate'),
	url(r'^view/$','view'),
	)