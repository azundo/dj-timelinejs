# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db import transaction
from .models import Timeline, TimelineImporter
from .forms import TimelineForm

def timelines(request):
    """List timelines"""

    timelines = Timeline.objects.filter(published=True)
    if not request.user.is_authenticated():
        timelines = timelines.filter(private=False)
    return render(request, 'timeline/timelines.html', {'timelines': timelines})

def timeline(request, slug):
    """Show a timeline"""
    timeline = get_object_or_404(Timeline, slug=slug)
    if timeline.private and not request.user.is_authenticated():
        raise PermissionDenied
    if not timeline.published:
        raise Http404
    return render(request, 'timeline/timeline.html', {'timeline': timeline})

@login_required
@transaction.commit_manually
def import_timeline_from_spreadsheet(request):
    """
    Manually manage the transaction so we can roll back any TimelineItems
    and the Timeline itself if any of the items fail.
    """
    if request.method == 'GET':
        form = TimelineForm()
    elif request.method == 'POST':
        form = TimelineForm(request.POST)
        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.slug = slugify(timeline.title)
            timeline.save()
            try:
                importer = TimelineImporter(form.cleaned_data['item_data'], timeline)
                errors = importer.import_items()
            except Exception, e:
                messages.add_message(request, messages.ERROR, 'Importing your timeline data failed with error: %s' % e)
                transaction.rollback()
                return redirect(reverse('timelines'))
            for error in errors:
                messages.add_message(request, messages.WARNING, error)
            transaction.commit()
            return redirect(timeline.get_absolute_url())
    # render hits the database (I think due to django_compressor) so we need
    # to close our transaction after the render call
    response = render(request, 'timeline/import_timeline.html', {'form': form})
    transaction.commit()
    return response
