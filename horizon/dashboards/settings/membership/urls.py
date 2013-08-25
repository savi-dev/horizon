# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf.urls.defaults import *

from .join import urls as join_urls
from .views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'join/', include(join_urls, namespace='join')),
)
