# -*- coding: utf-8 -*-

import abc
import json

from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import Textarea
from django.utils.translation import ugettext_lazy

_FIELD_TYPES_DICT = {}

_FIELD_TYPE_CHOICES = []

__all__ = [
    'register_field_type', 'get_field', 'get_field_type_choices',
    'DynamicFieldController',
    'ChoiceField'
]

def register_field_type(name):
    def wrapper(clazz):
        clazz.FIELD_NAME = name
        field = clazz()
        _FIELD_TYPES_DICT[name] = field
        _FIELD_TYPE_CHOICES.append((name, field.get_type_description()))
        return clazz
    return wrapper

def get_field(name):
    """
    :param str name:
    :return: Returns field type by name
    :rtype: :class:`DynamicFieldController`
    """
    return _FIELD_TYPES_DICT[name]

def get_field_type_choices():
    """
    Returns django choices dictionary containing dynamic fields.
    """
    return _FIELD_TYPE_CHOICES

class DynamicFieldController(object, metaclass=abc.ABCMeta):

    FIELD_NAME = None

    @abc.abstractmethod
    def get_type_description(self):
        return None

    def load_field(self, dynamic_field):
        field = self.create_field()
        field.required = dynamic_field.required
        return field

    @abc.abstractmethod
    def create_field(self):
        return None

class _DjangoDynamicFieldController(DynamicFieldController):

    DESCRIPTION = None

    DJANGO_FIELD_TYPE = None

    def get_type_description(self):
        return self.DESCRIPTION


    def create_field(self):
        return self.DJANGO_FIELD_TYPE()

def create_django_dynamic_field(django_type, description):

    clazz = type("Dynamic"+django_type.__name__, (_DjangoDynamicFieldController, ), {
        "DESCRIPTION": description,
        "DJANGO_FIELD_TYPE": django_type
    })

    register_field_type(django_type.__name__)(clazz)


create_django_dynamic_field(forms.IntegerField, ugettext_lazy('Number Field'))
create_django_dynamic_field(forms.CharField, ugettext_lazy('String Field'))
create_django_dynamic_field(forms.EmailField, ugettext_lazy('E-mail Field'))
create_django_dynamic_field(forms.DateField, ugettext_lazy('Date Field'))
create_django_dynamic_field(forms.BooleanField, ugettext_lazy('Yes/No Field'))

@register_field_type("TextField")
class DynamicTextField(_DjangoDynamicFieldController):

    DESCRIPTION = ugettext_lazy("Text Field")
    DJANGO_FIELD_TYPE = forms.CharField

    def create_field(self):
        field =  super().create_field()
        field.widget = Textarea()
        return field

@register_field_type("ChoicesField")
class ChoicesField(_DjangoDynamicFieldController):

    DESCRIPTION = ugettext_lazy("ComboBox Field")
    DJANGO_FIELD_TYPE = ChoiceField

    def has_choice(self, dynamic_field, name):
        choices = [c.lower() for c in self.get_choices(dynamic_field)]
        return name.lower() in choices

    def get_choices(self, dynamic_field):
        """
        :param dynamic_field:
        :type dynamic_field: :class:`dynamic_forms.models.DynamicFormField`
        :return: List containing possible choices (strings)
        """
        if dynamic_field.additional_data is None:
            return []
        json_str = dynamic_field.additional_data.get("choices", "[]")
        return json.loads(json_str)

    def set_choices(self, dynamic_field, choices):

        choices = list(choices)

        for ch in choices:
            if not isinstance(ch, str):
                raise ValueError("Choices must be strings, {} is {}".format(ch, type(ch)))

        dynamic_field.additional_data['choices'] = choices


    def add_choice(self, dynamic_field, choice):

        if self.has_choice(dynamic_field, choice):
            raise ValueError("Field already contains choice '{}'".format(choice))

        choices = self.get_choices(dynamic_field)
        choices.append(choice)
        self.set_choices(dynamic_field, choices)


    def load_field(self, dynamic_field):
        choice_field = super().load_field(dynamic_field)
        choices = [(c, c) for c in self.get_choices(dynamic_field)]
        if not dynamic_field.required:
            choices.insert(0, ('', "-"*7))
        choice_field.choices = choices
        return choice_field

