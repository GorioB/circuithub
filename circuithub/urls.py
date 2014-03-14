from django.conf.urls import patterns, include, url
from django.conf import settings #for serving static files
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()


urlpatterns= patterns('',
    # Examples:
    # url(r'^$', 'logintest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^upload/',include('upload.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^u/',include('circuits.urls')),
    url(r'^dbman/',include('pricing.urls')),
    url(r'^login/','loginapp.views.login_view'),
    url(r'^logout/','loginapp.views.logout_view'),
    url(r'^$','loginapp.views.index_view'),
    url(r'^register/','loginapp.views.register'),
    url(r'^register_submit/','loginapp.views.register_submit'),
)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #for serving static files
