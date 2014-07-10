# -*- coding: utf-8 -*-
from _operator import itemgetter
from functools import partial
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms.fields import ChoiceField
from django.utils.translation import ugettext_lazy

from localflavor.pl import forms as plforms
from localflavor.pl.pl_administrativeunits import ADMINISTRATIVE_UNIT_CHOICES
from localflavor.pl.pl_voivodeships import VOIVODESHIP_CHOICES
from dynamic_forms.fieldtype import create_dynamic_field_from_django_form, \
    create_dynamic_field_from_a_callable


class NipOrPeselField(forms.Field):
    """
    This is a field that accepts either NIP or PESEL field --- can be usefull
    for invoices where (for some time) you can specify either number to
    identify a person for the invoice.
    """

    default_error_messages = {
        'invalid': ugettext_lazy(
            "Please provide either a valid NIP number or a valid PESEL number. "
            "PESEL number should be provided as 11-digit string: 01234567891. "
            "NIP can be specified either as 10-digit string or as: XXX-XXX-XX-XX, XXX-XX-XX-XXX."
        )
    }

    def __try_nip(self, value):
        nip_field = plforms.PLNIPField()
        try:
            return nip_field.clean(value)
        except ValidationError:
            return None

    def __try_pesel(self, value):
        nip_field = plforms.PLPESELField()
        try:
            return nip_field.clean(value)
        except ValidationError:
            return None

    def clean(self, value):
        value = super().clean(value)
        if value in EMPTY_VALUES:
            return ''
        candidate = self.__try_nip(value)
        if candidate is None:
            candidate = self.__try_pesel(value)
        if candidate is None:
            raise ValidationError(self.error_messages['invalid'])


create_dynamic_field_from_django_form(plforms.PLPESELField, ugettext_lazy('PESEL number'))
create_dynamic_field_from_django_form(plforms.PLNIPField, ugettext_lazy('NIP number'))
create_dynamic_field_from_django_form(plforms.PLPostalCodeField, ugettext_lazy('Postal number'))
create_dynamic_field_from_django_form(plforms.PLNationalIDCardNumberField, ugettext_lazy('Polish ID card number'))
create_dynamic_field_from_django_form(NipOrPeselField, ugettext_lazy('PESEL or NIP number'))
create_dynamic_field_from_a_callable(
    partial(ChoiceField, choices=VOIVODESHIP_CHOICES),
    "PolishProvince", ugettext_lazy('Polish Province'))
create_dynamic_field_from_a_callable(
    partial(ChoiceField,
            choices=sorted(ADMINISTRATIVE_UNIT_CHOICES, key=itemgetter(0))),
    "PolishCounty", ugettext_lazy('Polish County'))
