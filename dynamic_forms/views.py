from django.shortcuts import render_to_response
from dynamic_forms.forms import AddDynamicFormField, BaseDynamicForm,\
    AddChoices
from dynamic_forms.models import DynamicForm, DynamicFormData, DynamicFormField
from django.template import RequestContext
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import json

#CR: Nie lubicie ClassBasedViews? IMO są super!

#CR: Nie jestem przekonany że w tym miejscu powinniśmy robić walidację
#uprawnień. Zapewne Drigan będzie potrzebował innego zestawu uprwanień
#a może ktoś gdzieś nie będize potrzebował @login_required...
# Chyba że django-guardian to załatwia
@login_required
def add_dynamic_form(request, content_type_model, object_id):
    #CR: Pozbycie się GenericForeignKeys z DynamicForm znacznie uprościłoby
    #ten widok
    if request.method == 'POST':
        content_type = ContentType.objects.get(model=content_type_model)
        dynamic_form = DynamicForm.objects.create(content_type=content_type,
                                                  object_id=object_id)
        return http.HttpResponseRedirect(reverse(
            'dynamic_forms.views.add_dynamic_form_field',
            args=(dynamic_form.id,)))


@login_required
def edit_dynamic_form(request, dynamic_form_id):
    dynamic_form = get_object_or_404(DynamicForm, pk=dynamic_form_id)
    return render_to_response("dynamic_forms/dynamic_form_edit.html",
                              {"dynamic_form": dynamic_form},
                              context_instance=RequestContext(request))


@login_required
def change_field_order(request, field_id, direction):
    field = get_object_or_404(DynamicFormField, pk=field_id)
    if request.method == "POST":
        field.position += int(direction)
        field.save()
        messages.success(request, _('Order has been changed.'))
    return http.HttpResponseRedirect(reverse(
        'dynamic_forms.views.edit_dynamic_form',
        args=(field.form.id,)))


@login_required
def add_dynamic_form_field(request, dynamic_form_id):
    dynamic_form = get_object_or_404(DynamicForm, pk=dynamic_form_id)
    if request.method == 'POST':
        form = AddDynamicFormField(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            #CR: Totalnie nie rozumiem tego ifa? Może wyjaśnienie.
            #Dlaczego to nie jest dynamic_form.fields.filter ... ?
            if not DynamicFormField.objects.filter(name__iexact=field.name):
                field.form = dynamic_form
                field.save()
                form.save()
                if field.field_type == 'ChoiceField':
                    field.additional_data = {'choices': []}
                    field.save()
                    return http.HttpResponseRedirect(reverse(
                        'dynamic_forms.views.add_choices_to_choicefield',
                        args=(field.id,)))
                form = AddDynamicFormField()
                messages.success(request,
                                 _('Field has been added successfully.'))
            else:
                messages.error(request,
                               _('Field with this name already exists.'))
    else:
        form = AddDynamicFormField()
    dynamic_form_form = BaseDynamicForm(dynamic_form)
    return render_to_response("dynamic_forms/dynamic_form_add.html",
                              {"form": form,
                               "dynamic_form": dynamic_form,
                               "dynamic_form_form": dynamic_form_form},
                              context_instance=RequestContext(request))


@login_required
def delete_dynamic_form_field(request, field_id):
    dynamic_form_field = get_object_or_404(DynamicFormField, pk=field_id)
    if request.method == "POST":
        dynamic_form_field.delete()
        messages.success(request, _('Field has been deleted.'))
    return http.HttpResponseRedirect(reverse(
        'dynamic_forms.views.edit_dynamic_form',
        args=(dynamic_form_field.form.id,)))


@login_required
def add_choices_to_choicefield(request, field_id):
    choice_field = get_object_or_404(DynamicFormField, pk=field_id)
    if request.method == 'POST':
        form = AddChoices(request.POST)
        if form.is_valid():
            new_choice = form.cleaned_data['name']
            print(repr(choice_field.additional_data))
            choices = json.loads(choice_field.additional_data['choices'])
            choices_lowercase = [choice.lower() for choice in choices]
            if not new_choice.lower() in choices_lowercase:
                choices.append(new_choice)
                choice_field.additional_data['choices'] = choices
                choice_field.save()
                form = AddChoices()
                messages.success(request,
                                 _('Choice has been added successfully.'))
            else:
                messages.error(request,
                               _('This choice already exists.'))

    else:
        form = AddChoices()
    return render_to_response("dynamic_forms/choices_add.html",
                              {"form": form,
                               "dynamic_form_id": choice_field.form.id},
                              context_instance=RequestContext(request))

#CR: Tutaj @login_required zostaje, używamy request.user? Choć: anonimowe ankiety?
@login_required
def fill_form(request, dynamic_form_id):
    dynamic_form = get_object_or_404(DynamicForm, pk=dynamic_form_id)
    if request.method == 'POST':
        form = BaseDynamicForm(dynamic_form, request.POST)
        if form.is_valid():
            DynamicFormData.objects.create(form=dynamic_form,
                                           user=request.user,
                                           data=form.cleaned_data)
            messages.success(request,
                             _('Form has been filled successfully.'))
            return http.HttpResponseRedirect(reverse(
                'dynamic_forms.views.participants_list',
                args=(dynamic_form_id,)))
    else:
        form = BaseDynamicForm(dynamic_form)
    return render_to_response("dynamic_forms/form_fill.html",
                              {"dREJCEN-87ynamic_form": dynamic_form,
                               "dynamic_form_form": form},
                              context_instance=RequestContext(request))


#CR: To chyba nie należy do tej aplikacji? Chyba że participant to lista
#osób które wypełniłyu ankietę?
@login_required
def participants_list(request, dynamic_form_id):
    dynamic_form = get_object_or_404(DynamicForm, pk=dynamic_form_id)
    participants = DynamicFormData.objects.all().filter(form=dynamic_form)
    return render_to_response("dynamic_forms/list.html",
                              {"participants": participants},
                              context_instance=RequestContext(request))
