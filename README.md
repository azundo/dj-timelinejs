dj-timelinejs
=============

Support for TimelineJS served through Django.

**Features**

* Support for markdown in slide content
* Media storage in Django
* Import existing TimelineJS Google Spreadsheets
* Private/Public and Published/Unpublished timeline states

**Basic Usage**

This package supplies Django models and Class-Based-Views which make it easy to
save and serve up TimelineJS content from a Django site.

***Overriding URLS and Templates***

You probably want to do your own url and template configuration. Class-Based-Views makes this easy.

```python
# your urls.py
from timelinejs.views import TimelineListView, \
    TimelineDeTailView, ImportTimelineFromSpreadsheetView

urls = patterns(''
    (
        r'^/$',
        TimelineListView.as_view(template_name='list_template_name.html'),
        name='timelines',
    ),
    (
        r'^import/$',
        ImportTimelineFromSpreadsheetView.as_view(template_name='import_template_name.html'),
        name='import_timeline',
    ),
    (
        r'^(?P<slug>[a-zA-Z0-9-_]+)/$',
        TimelineView.as_view(template_name='detail_template_name.html'),
        name='timeline',
    ),
)
```

Use the included templates as a sample and adjust based on your template setup.
There is no templatetag support since the configuration of TimelineJS is
complicated and you may want to use tools such as django_compressor for static
assest. A `Timeline` instance does have a `source` property which prints the
Google Spreadsheet URL if your timeline is linked to a Google Spreadsheet, or
outputs the appropriate JSON generated from Django models. Use `timeline.html`
as a reference, but many more config options are available, see the TimelineJS
documentation.

***Adding Timelines***

Use the import function to import from existing Google Spreadsheets, or use the
Django Admin interface to input Timeline details.

***Permissions***

On top of the default permissions (add, change, remove which apply through the
Django admin) dj-timelinejs includes a `view_private_timelines` permission that
toggles whether or not a user sees private timelines.

Users with the `add_timeline` permission will also be allowed to use the import
function, and a `user_can_add_timelines` context variable is passed to the
`TimlineListView` if you wish to include a link to the admin page for adding
timelines. See the timelines.html template as an example.


