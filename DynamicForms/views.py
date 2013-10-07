from django.shortcuts import render_to_response
from DynamicForms.forms import AddDynamicFormField
from DynamicForms.models import DynamicForm
from django.template import RequestContext
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


@login_required
def add_dynamic_form(request, content_type_model, object_id):
    content_type = ContentType.objects.get(model=content_type_model)
    dynamic_form = DynamicForm.objects.create(content_type=content_type,
                                              object_id=object_id)
    return http.HttpResponseRedirect(reverse(
        'DynamicForms.views.add_dynamic_form_field',
        args=(dynamic_form.id,)))


@login_required
def add_dynamic_form_field(request, dynamic_form_id):
    dynamic_form = get_object_or_404(DynamicForm, pk=dynamic_form_id)
    if request.method == 'POST':
        form = AddDynamicFormField(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.form = dynamic_form
            field.save()
            form.save()
            form = AddDynamicFormField()
            messages.success(request,
                             _('Field has been added successfully.'))
    else:
        form = AddDynamicFormField()
    return render_to_response("DynamicForms/dynamic_form_add.html",
                              {"form": form, "dynamic_form": dynamic_form},
                              context_instance=RequestContext(request))
