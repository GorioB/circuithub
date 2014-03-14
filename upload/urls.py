from django.conf.urls import patterns, include, url

urlpatterns = patterns('upload.views',
	url(r'^$','upload'),
	url(r'^view/$','userUpload'),
	url(r'^manual/$','manual'),
	url(r'^manual/submit/$','manualUpload')
	)