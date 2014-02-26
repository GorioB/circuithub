from django.conf.urls import patterns, include, url

urlpatterns = patterns('circuits.views',
	url(r'(?P<owner_id>\S+)/circuit/(?P<list_id>\S+)/$','listRawContents'),
	url(r'(?P<owner_id>\S+)/$','listRawLists'),
	)