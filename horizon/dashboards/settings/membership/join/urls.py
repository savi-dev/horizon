# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on July 23, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''
from django.conf.urls.defaults import patterns, url

from .views import CreateProjectView


urlpatterns = patterns('',
    url(r'^create/$', CreateProjectView.as_view(), name='create'),)
