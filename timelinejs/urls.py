from django.conf.urls import patterns, url

urlpatterns = patterns('timeline.views',
    url(r'^$', 'timelines', name='timelines'),
    url(r'^import/$', 'import_timeline_from_spreadsheet', name='import_timeline_from_spreadsheet'),
    url(r'^(?P<slug>[a-zA-Z0-9-_]+)/$', 'timeline', name='timeline'),
)
