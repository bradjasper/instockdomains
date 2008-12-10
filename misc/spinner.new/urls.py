from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
		(r'^spinner/', include('instockdomains.spinner.urls')),
		(r'^scripts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/###/templates/scripts/'}),
    (r'^admin/(.*)', admin.site.root),
)