# -*- coding: utf-8 -*-

"""
Dynamic forms module.

Models diagram:

.. figure: dynamic_forms/dynamic_forms.png

    Dynamic forms UML diagram
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django_hstore import hstore
from positions import PositionField

from . import default_fieldtypes # For side effect

from .fieldtype import get_field_type_choices, get_field

class FieldNameNotUnique(ValueError): pass

class DynamicForm(models.Model):

    """
    Represents a dynamic form that is a form for which fields
    can be added dynamically.
    """


    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey(
        'content_type', 'object_id')
    """
    Reference to object that uses this instance of Dynamic Form
    """

    def add_field_to_form(self, field):

        if self.fields.filter(name__iexact = field.name).exists():
            raise FieldNameNotUnique("Field with the same name is already added to a form")

        field.form = self

class DynamicFormField(models.Model):

    """
    Single field in a dynamic form
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of the field, it will be displayed as label "
                  "for this question")

    field_type = models.CharField(
        max_length=100, choices=get_field_type_choices(),
        help_text = "Type of data this field stores")

    required = models.BooleanField(default=True)
    form = models.ForeignKey(DynamicForm, related_name='fields')
    """
    Form for which this object
    """
    additional_data = hstore.DictionaryField(blank=True, null=False, default=lambda : {})
    """
    Dictionary of additional data, contents are defined by:
    :attr:`DynamicFormField.field_type`
    """
    position = PositionField(collection='form')
    objects = hstore.HStoreManager()

    def get_django_field(self):
        return self.dynamic_field.load_field(self)

    @property
    def dynamic_field(self):
        """
        Returns instance of :class:`DynamicFieldController`, object
        that encapsulates behaviour of this field.

        It is depenedent on `DynamicFormField.field_type`
        :return: :class:`DynamicFieldController`,
        :rtype: :class:`DynamicFieldController`,
        """
        return get_field(self.field_type)

    class Meta:
        ordering = ['position']



class DynamicFormData(models.Model):
    """
    Response to dynamic form
    """
    form = models.ForeignKey(DynamicForm)
    user = models.ForeignKey(User)
    data = hstore.DictionaryField(db_index=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return u'%s %s' % (self.form, self.user)
