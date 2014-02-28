from django.conf.urls import patterns, include, url

urlpatterns = patterns('circuits.views',
	url(r'^(?P<owner_id>\S+)/(?P<list_id>\S+)/(?P<circuit_name>\S+)/delete/$','deleteCheckList'),
	url(r'^(?P<owner_id>\S+)/(?P<list_id>\S+)/delete/$','deleteRawList'),
	url(r'^(?P<owner_id>\S+)/(?P<list_id>\S+)/(?P<circuit_name>\S+)/update/$','updateChecklist'),
	url(r'^(?P<owner_id>\S+)/(?P<list_id>\S+)/checkout/$','createChecklist'),
	url(r'^(?P<owner_id>\S+)/(?P<list_id>\S+)/(?P<circuit_name>\S+)/$','listCircuitContents'),
	url(r'^(?P<owner_id>\S+)/(?P<list_id>\S+)/$','listRawContents'),
	url(r'^(?P<owner_id>\S+)/$','listRawLists'),
	)