from django.shortcuts import redirect, render
from django.utils.lru_cache import lru_cache
from wagtail.wagtailadmin import messages
from wagtail.wagtailadmin.edit_handlers import (ObjectList,
                                                extract_panel_definitions_from_model_class)
from wagtail.wagtailcore.models import Site

from .models import SiteMetadataPreferences


@lru_cache()
def get_edit_handler(model):
    panels = extract_panel_definitions_from_model_class(model, ['site'])
    return ObjectList(panels).bind_to_model(model)


def index(request):
    site = Site.find_for_request(request)
    instance = SiteMetadataPreferences.objects.filter(site=site).first()
    if instance is None:
        instance = SiteMetadataPreferences(site=site)
    EditHandler = get_edit_handler(SiteMetadataPreferences)
    SiteMetadataPreferencesForm = EditHandler.get_form_class(SiteMetadataPreferences)

    if request.method == "POST":
        form = SiteMetadataPreferencesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'The form has been successfully saved.')
            return redirect('wagtailmetadata')
        else:
            messages.error(request, 'The form could not be saved due to validation errors')
    else:
        form = SiteMetadataPreferencesForm(instance=instance)

    edit_handler = EditHandler(instance=instance, form=form)

    return render(request, 'wagtailmetadata/index.html', {
        'form': form,
        'edit_handler': edit_handler,
    })
