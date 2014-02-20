from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'logintest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/','loginapp.views.login_view'),
    url(r'^logout/','loginapp.views.logout_view'),
    url(r'^$','loginapp.views.index_view'),
    url(r'^register/','loginapp.views.register'),
    url(r'^register_submit/','loginapp.views.register_submit')
)
