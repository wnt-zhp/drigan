from django.db import models
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django_hstore import hstore


FIELD_TYPES = [
    ('IntegerField', 'Number Field'),
    ('CharField', 'String Field'),
    ('TextField', 'Text Field'),
    ('EmailField', 'E-mail Field'),
    ('DateField', 'Date Field'),
    ('BooleanField', 'Yes/No Field')
]


types = {'IntegerField': forms.IntegerField(),
         'CharField': forms.CharField(max_length=100),
         'TextField': forms.CharField(widget=forms.Textarea),
         'EmailField': forms.EmailField(),
         'DateField': forms.DateField(),
         'BooleanField': forms.BooleanField()
         }


class DynamicForm(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.content_object.__unicode__()

    def to_form(self):
        return BaseDynamicForm(self)


class DynamicFormField(models.Model):
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    form = models.ForeignKey(DynamicForm, related_name='fields')

    def __unicode__(self):
        return u'%s: %s' % (self.form.__unicode__(), self.name)


class BaseDynamicForm(forms.Form):

    def __init__(self, DynamicForm, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        dynamic_form = DynamicForm
        dynamic_fields = DynamicFormField.objects.filter(form=dynamic_form)
        for dynamic_field in dynamic_fields:
            field_type = types[dynamic_field.field_type]
            field_type.required = dynamic_field.required
            self.fields[dynamic_field.name] = field_type


class DynamicFormData(models.Model):
    form = models.ForeignKey(DynamicForm)
    user = models.ForeignKey(User)
    data = hstore.DictionaryField(db_index=True)

    def __unicode__(self):
        return u'%s %s' % (self.form, self.user)
