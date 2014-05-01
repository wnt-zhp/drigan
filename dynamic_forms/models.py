# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django_hstore import hstore
from positions import PositionField

FIELD_TYPES = [
    ('IntegerField', 'Number Field'),
    ('CharField', 'String Field'),
    ('TextField', 'Text Field'),
    ('EmailField', 'E-mail Field'),
    ('DateField', 'Date Field'),
    ('BooleanField', 'Yes/No Field'),
    ('ChoiceField', 'Choice Field'),
]


class DynamicForm(models.Model):
    """
    Dynamic form
    """

    #CR: Nie byłoby czyściej gdyby to co posiada DynamicForm miało zwykłego
    # FK do Dynamic form?
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        #CR: Dlaczego DynamicForm renderuje się jako obiekt który go posiada

        return self.content_object.__unicode__()


class DynamicFormField(models.Model):
    """
    Field in dynamic form
    """
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    form = models.ForeignKey(DynamicForm, related_name='fields')
    additional_data = hstore.DictionaryField(blank=True, null=True)
    position = PositionField(collection='form')

    objects = hstore.HStoreManager()

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return u'%s: %s' % (self.form.__unicode__(), self.name)


class DynamicFormData(models.Model):
    """
    Response for dynamic form.
    """
    form = models.ForeignKey(DynamicForm)
    user = models.ForeignKey(User)
    data = hstore.DictionaryField(db_index=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return u'%s %s' % (self.form, self.user)
