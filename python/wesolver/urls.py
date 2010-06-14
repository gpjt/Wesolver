from os.path import join

from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'ui/login.html'}),
    (r'^user/', include('wesolver.ui.urls')),
)


if settings.ENVIRONMENT == "dev":
    urlpatterns += patterns("django.views",
        url(
            r"^$",
            "static.serve",
            {
                "document_root" : join(settings.TOP_ROOT_DIR, 'dev-root-html'),
                "path" : "index.html"
            }
        ),
        url(
            r"ext-js/(?P<path>.*)/$" ,
            "static.serve",
            {"document_root": join(settings.TOP_ROOT_DIR, "html", 'ext-js')}
        ),
    )

