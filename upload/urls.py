from django.conf.urls import patterns, include, url
from django.conf import settings #for serving static files
from django.contrib import admin


urlpatterns= patterns('upload.views',
    url(r'^list/$','list',name='list'),
)
