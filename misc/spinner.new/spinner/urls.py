from django.conf.urls.defaults import *

#urlpatterns = patterns('instockdomains.spinner.views',
#		(r'^$', 'index'),
#		(r'^(?P<query>\s+)/$', 'search'),
#)

urlpatterns = patterns('instockdomains.spinner.views',
    (r'^$', 'index'),
		(r'^search', 'search'),
		(r'^results', 'results'),
		(r'^synonyms', 'synonyms')
)