from os.path import join

from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^user/', include('wesolver.ui.urls')),
)


if settings.ENVIRONMENT == "dev":
    urlpatterns += patterns("django.views",
        url(
            r"^$",
            "static.serve",
            {
                "document_root" : join(settings.ROOT_DIR, 'dev-site-index'),
                "path" : "index.html"
            }
        ),
        url(
            r"ext-js/(?P<path>.*)/$" ,
            "static.serve",
            {"document_root": join(settings.ROOT_DIR, 'ext-js')}
        ),
    )

