# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, \
    DeleteView, CreateView
from django.views.generic.list import ListView

from django.template import RequestContext
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


from guardian.mixins import LoginRequiredMixin
from dynamic_forms.fieldtype import ChoicesField

from dynamic_forms.forms import AddDynamicFormField, BaseDynamicForm,\
    AddChoices
from dynamic_forms.models import DynamicForm, DynamicFormData, DynamicFormField, \
    FieldNameNotUnique


class AddDynamicForm(LoginRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, content_type_model, object_id):

        content_type = ContentType.objects.get(model=content_type_model)
        get_object_or_404(content_type.model_class(), pk=object_id)
        dynamic_form = DynamicForm.objects.create(content_type=content_type,
                                                  object_id=object_id)



        return http.HttpResponseRedirect(reverse(
            'dynamic_forms.views.add_dynamic_form_field',
            args=(dynamic_form.id,)))

@login_required
def add_dynamic_form_simple(request):
    dynamic_form = DynamicForm.objects.create()
    return http.HttpResponseRedirect(reverse(
            'dynamic_forms.views.add_dynamic_form_field',
            args=(dynamic_form.id,)))

class EditDynamicForm(LoginRequiredMixin, DetailView):

    http_method_names = ['get']
    pk_url_kwarg = 'dynamic_form_id'
    model = DynamicForm
    template_name = "dynamic_forms/dynamic_form_edit.html"
    context_object_name="dynamic_form"


class ChangeFieldOrder(LoginRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, field_id, direction):
        field = get_object_or_404(DynamicFormField, pk=field_id)
        field.position += int(direction)
        field.save()
        messages.success(request, _('Order has been changed.'))
        return http.HttpResponseRedirect(reverse(
            'dynamic_forms.views.edit_dynamic_form',
                args=(field.form.id,)))


class AddDynamicFormFieldView(LoginRequiredMixin, CreateView):

    template_name = "dynamic_forms/dynamic_form_add.html"
    form_class = AddDynamicFormField

    def dispatch(self, request, *args, **kwargs):
        self.dynamic_form = get_object_or_404(DynamicForm, pk=kwargs['dynamic_form_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'dynamic_form': self.dynamic_form,
            'dynamic_form_form': BaseDynamicForm(self.dynamic_form)
        })
        return kwargs

    def get_success_url(self):
        return reverse('dynamic_forms.views.add_dynamic_form_field',
                                kwargs={"dynamic_form_id":self.dynamic_form.id})


    def form_valid(self, form):
        field = form.save(commit=False)
        try:
            self.dynamic_form.add_field_to_form(field)
            field.save()
            messages.success(self.request,
                             _('Field has been added successfully.'))
        except FieldNameNotUnique:
            messages.error(self.request,
                           _('Field with this name already exists.'))
            return self.form_invalid(form)

        if field.field_type == ChoicesField.FIELD_NAME:
            # TODO: This should really be handled somewhere else
            return http.HttpResponseRedirect(reverse(
                'dynamic_forms.views.add_choices_to_choicefield',
            args=(field.id,)))

        return super().form_valid(form)

class DeleteDynamicFormField(LoginRequiredMixin, DeleteView):

    http_method_names = ['post']
    pk_url_kwarg = 'field_id'
    model = DynamicFormField

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Field has been deleted.'))
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dynamic_forms.views.edit_dynamic_form', args=(self.object.form.pk,))


class AddChoicesToChoiceField(LoginRequiredMixin, FormView):

    http_method_names = ['get', 'post']
    pk_url_kwarg = 'field_id'
    model = DynamicFormField
    form_class = AddChoices
    template_name = "dynamic_forms/choices_add.html"

    def dispatch(self, request, *args, **kwargs):
        self.choice_field = get_object_or_404(DynamicFormField, pk=kwargs['field_id'], field_type=ChoicesField.FIELD_NAME)
        self.dynamic_form_id = self.choice_field.form.id
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            dynamic_form_id=self.dynamic_form_id,
            field_id = self.kwargs['field_id'],
            **kwargs
        )

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        new_choice = form.cleaned_data['name']
        choice_field = self.choice_field
        if not choice_field.dynamic_field.has_choice(choice_field, new_choice):
            choice_field.dynamic_field.add_choice(choice_field, new_choice)
            choice_field.save()
            messages.success(self.request,
                             _('Choice has been added successfully.'))
            return super().form_valid(form)
        else:
            messages.error(self.request,
                               _('This choice already exists.'))
            return super().form_invalid(form)

class FillForm(LoginRequiredMixin, FormView):

    form_class = BaseDynamicForm
    template_name = "dynamic_forms/form_fill.html"

    def get_success_url(self):
        return reverse('dynamic_forms.views.participants_list',
                args=(self.dynamic_form.pk,))

    def dispatch(self, request, *args, **kwargs):
        self.dynamic_form = get_object_or_404(DynamicForm, pk=kwargs['dynamic_form_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['dynamic_form'] = self.dynamic_form
        return kwargs

    def form_valid(self, form):
        DynamicFormData.objects.create(form=self.dynamic_form,
                                       user=self.request.user,
                                       data=form.cleaned_data)
        messages.success(self.request,
                         _('Form has been filled successfully.'))
        return super().form_valid(form)

class ParticipantList(LoginRequiredMixin, ListView):

    http_method_names = ['get']
    template_name = "dynamic_forms/list.html"
    context_object_name = "participants"

    def dispatch(self, request, *args, **kwargs):
        self.dynamic_form = get_object_or_404(DynamicForm, pk=kwargs['dynamic_form_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return DynamicFormData.objects.filter(form=self.dynamic_form)

