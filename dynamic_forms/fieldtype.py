# -*- coding: utf-8 -*-

import abc
import json

from django import forms
from django.forms.fields import ChoiceField, Field
from django.forms.widgets import Textarea
from django.utils.translation import ugettext_lazy


_FIELD_TYPES_DICT = {}

_FIELD_TYPE_CHOICES = []

__all__ = [
    'register_field_type', 'get_field', 'get_field_type_choices',
    'DynamicFieldController',
    'ChoiceField'
]


#TODO: We really should store types and instantiate them during
# DynamicFormField.field_type property call, in this case
# to DynamicFormField could be stored inside instance of new class.
# Now we store instances --- which could wreak havoc if any of them
# store request state.
def register_field_type(name):
    """
    Registers field type for name if you decorate a type with it

    >>> @register_field_type("OtherChoicesField")
    ... class OtherChoicesField(ChoicesField): pass

    >>> isinstance(get_field("OtherChoicesField"), OtherChoicesField)
    True

    :param name: Name under which to store decorated type
    """
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

    """
    Main class of this API. It is responsible for creating dynamic fields
    from the database.

    """

    FIELD_NAME = None
    """
    A class variable. subclasses **must** override this
    as this field defines type of the field that particular subclass
    will create. This is a string.
    """

    @abc.abstractmethod
    def get_type_description(self):
        """

        :return: Returns human redable description of this controller.
        :rtype: :class:`str`
        """
        return None

    def load_field(self, dynamic_field):
        """
        Creates django field from this dynamic field. This metod takes
        care of common operations done for all fields. Subclasses need
        to override :meth:`DynamicFieldController._create_field`.

        :param dynamic_field:
        :return: Django field
        :rtype: Subclass of :class:`django.forms.fields.Field`
        """
        field = self._create_field()
        field.required = dynamic_field.required
        return field

    @abc.abstractmethod
    def _create_field(self):
        """
        Creates django field from this dynamic field. This should not be called
        directly in favour of: :meth:`DynamicFieldController.load_field`.

        This should be overriden.

        :return: Django field
        :rtype: Subclass of :class:`django.forms.fields.Field`
        """
        return None


class _DjangoDynamicFieldController(DynamicFieldController):
    """
    DynamicFormController that simply wraps a DjangoField.

    :cvar type DJANGO_FIELD_TYPE: Type of the django field stored by this
        Controller.
    :cvar str DESCRIPTION: Human readable description of the field.
    """

    DESCRIPTION = None

    DJANGO_FIELD_TYPE = Field

    def get_type_description(self):
        return self.DESCRIPTION

    def _create_field(self):
        return self.DJANGO_FIELD_TYPE()


def create_dynamic_field_from_django_form(django_type, description):

    """
    Creates a dynamic field from django field.
    :param type django_type: Type that will be wrapped.
    :param str description: Human readable desctiption
    :return: None
    """

    clazz = type("Dynamic" + django_type.__name__, (_DjangoDynamicFieldController, ), {
        "DESCRIPTION": description,
        "DJANGO_FIELD_TYPE": django_type
    })

    register_field_type(clazz.__name__)(clazz)


@register_field_type("DynamicTextField")
class DynamicTextField(_DjangoDynamicFieldController):

    DESCRIPTION = ugettext_lazy("Text Field")
    DJANGO_FIELD_TYPE = forms.CharField

    def _create_field(self):
        field = super()._create_field()
        field.widget = Textarea()
        return field


@register_field_type("DynamicChoicesField")
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
            choices.insert(0, ('', "-" * 7))
        choice_field.choices = choices
        return choice_field
