# Create your views here.
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db import transaction
from .models import Timeline, TimelineImporter
from .forms import TimelineForm

def timelines(request):
    """List timelines"""
    timelines = Timeline.objects.visible_to_user(request.user)
    return render(request, 'timelinejs/timelines.html', {'timelines': timelines})

def timeline(request, slug):
    """Show a timeline"""
    timeline = Timeline.objects.get_visible_to_user_or_404(user=request.user, slug=slug)
    return render(request, 'timelinejs/timeline.html', {'timeline': timeline})

@permission_required('timelinejs.add_timeline')
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
    response = render(request, 'timelinejs/import_timeline.html', {'form': form})
    transaction.commit()
    return response
