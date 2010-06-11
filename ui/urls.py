from django.conf.urls.defaults import *


urlpatterns = patterns('wesolver.ui.views',
    url(
        r'^(?P<username>[^/]+)/$',
        'user_page',
        {},
        name="show-user"
    ),

    url(
        r'^(?P<username>[^/]+)/(?P<sheet_id>\d+)$',
        'sheet_page',
        {},
        name="show-sheet"
    ),

)
