from django import forms
from django.utils.translation import ugettext_lazy
from dynamic_forms.fieldtype import create_dynamic_field_from_django_form

create_dynamic_field_from_django_form(forms.IntegerField, ugettext_lazy('Number Field'))
create_dynamic_field_from_django_form(forms.CharField, ugettext_lazy('String Field'))
create_dynamic_field_from_django_form(forms.EmailField, ugettext_lazy('E-mail Field'))
create_dynamic_field_from_django_form(forms.DateField, ugettext_lazy('Date Field'))
create_dynamic_field_from_django_form(forms.BooleanField, ugettext_lazy('Yes/No Field'))