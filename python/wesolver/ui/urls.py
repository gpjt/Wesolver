from django.conf.urls.defaults import *


urlpatterns = patterns('wesolver.ui.views',
    url(
        r'^(?P<username>[^/]+)/$',
        'user_page',
        {},
        name="show-user"
    ),

    url(
        r'^(?P<username>[^/]+)/createsheet/$',
        'create_sheet',
        {},
        name="create-sheet"
    ),

    url(
        r'^(?P<username>[^/]+)/(?P<sheet_id>\d+)/$',
        'sheet_page',
        {},
        name="show-sheet"
    ),

    url(
        r'^(?P<username>[^/]+)/(?P<sheet_id>\d+)/json$',
        'sheet_json',
        {},
        name="sheet-json"
    ),

    url(
        r'^(?P<username>[^/]+)/(?P<sheet_id>\d+)/update$',
        'sheet_update',
        {},
        name="sheet-update"
    ),

)
