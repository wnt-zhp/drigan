from django.shortcuts import render_to_response
from dynamic_forms.forms import AddDynamicFormField, BaseDynamicForm
from dynamic_forms.models import DynamicForm, DynamicFormData
from django.template import RequestContext
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import pickle


@login_required
def add_dynamic_form(request, content_type_model, object_id):
    if request.method == 'POST':
        content_type = ContentType.objects.get(model=content_type_model)
        dynamic_form = DynamicForm.objects.create(content_type=content_type,
                                                  object_id=object_id)
        return http.HttpResponseRedirect(reverse(
            'dynamic_forms.views.add_dynamic_form_field',
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
    dynamic_form_form = BaseDynamicForm(dynamic_form)
    return render_to_response("dynamic_forms/dynamic_form_add.html",
                              {"form": form,
                               "dynamic_form": dynamic_form,
                               "dynamic_form_form": dynamic_form_form},
                              context_instance=RequestContext(request))


@login_required
def fill_form(request, dynamic_form_id):
    dynamic_form = get_object_or_404(DynamicForm, pk=dynamic_form_id)
    if request.method == 'POST':
        form = BaseDynamicForm(dynamic_form, request.POST)
        if form.is_valid():
            filled_data = form.cleaned_data
            for k in filled_data:
                filled_data[k] = pickle.dumps(filled_data[k])
            DynamicFormData.objects.create(form=dynamic_form,
                                           user=request.user,
                                           data=filled_data)
            messages.success(request,
                             _('Form has been filled successfully.'))
            return http.HttpResponseRedirect("/")
    else:
        form = BaseDynamicForm(dynamic_form)
    return render_to_response("dynamic_forms/form_fill.html",
                              {"dynamic_form": dynamic_form,
                               "dynamic_form_form": form},
                              context_instance=RequestContext(request))
