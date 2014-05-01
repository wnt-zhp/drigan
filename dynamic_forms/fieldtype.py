# -*- coding: utf-8 -*-

import abc

from django import forms
from django.forms.widgets import Textarea
from django.utils.translation import ugettext_lazy

_FIELD_TYPES_DICT = {}

_FIELD_TYPE_CHOICES = []

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
    :rtype: :class:`DynamicFieldType`
    """
    return _FIELD_TYPES_DICT[name]

def get_field_choices():
    """
    Returns django choices dictionary containing dynamic fields.
    """
    return _FIELD_TYPE_CHOICES

class DynamicFieldType(object, metaclass=abc.ABCMeta):

    FIELD_NAME = None

    @abc.abstractmethod
    def get_type_description(self):
        return None

    @abc.abstractmethod
    def load_field(self, dynamic_field):
        return None

    @abc.abstractmethod
    def create_field(self):
        return None

class _DjangoDynamicField(DynamicFieldType):

    DESCRIPTION = None

    DJANGO_FIELD_TYPE = None

    def get_type_description(self):
        return self.DESCRIPTION

    def load_field(self, dynamic_field):
        field = self.create_field()
        field.required = dynamic_field.required
        return field

    def create_field(self):
        return self.DJANGO_FIELD_TYPE()

def create_django_dynamic_field(django_type, description):

    clazz = type("Dynamic"+django_type.__name__, (_DjangoDynamicField, ), {
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
class DynamicTextField(_DjangoDynamicField):

    DESCRIPTION = "Text Field"

    DJANGO_FIELD_TYPE = forms.CharField

    def create_field(self):
        field =  super().create_field()
        field.widget = Textarea()
        return field

# TODO: Add Choice Field
