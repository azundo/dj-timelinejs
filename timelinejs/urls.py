from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('timelinejs.views',
    url(r'^$', 'timelines', name='timelines'),
    url(r'^import/$', 'import_timeline_from_spreadsheet', name='import_timeline_from_spreadsheet'),
    url(r'^(?P<slug>[a-zA-Z0-9-_]+)/$', 'timeline', name='timeline'),
    url(r'^admin/', include(admin.site.urls)),
)
