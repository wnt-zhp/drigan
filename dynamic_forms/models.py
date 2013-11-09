from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django_hstore import hstore
import pickle

FIELD_TYPES = [
    ('IntegerField', 'Number Field'),
    ('CharField', 'String Field'),
    ('TextField', 'Text Field'),
    ('EmailField', 'E-mail Field'),
    ('DateField', 'Date Field'),
    ('BooleanField', 'Yes/No Field')
]


class DynamicForm(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.content_object.__unicode__()


class DynamicFormField(models.Model):
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    form = models.ForeignKey(DynamicForm, related_name='fields')

    def __unicode__(self):
        return u'%s: %s' % (self.form.__unicode__(), self.name)


class DynamicFormData(models.Model):
    form = models.ForeignKey(DynamicForm)
    user = models.ForeignKey(User)
    raw_data = hstore.DictionaryField(db_index=True)

    def __unicode__(self):
        return u'%s %s' % (self.form, self.user)

    def __init__(self, *args, **kwargs):
        super(DynamicFormData, self).__init__(*args, **kwargs)
        self.data = {}
        for k in self.raw_data:
                self.data[k] = pickle.loads(self.raw_data[k])
