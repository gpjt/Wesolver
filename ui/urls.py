from django.conf.urls.defaults import *


urlpatterns = patterns('wesolver.ui.views',
    (r'^(?P<username>[^/]+)/$', 'user_page'),
)
