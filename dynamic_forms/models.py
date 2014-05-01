from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django_hstore import hstore
from positions import PositionField

from .fieldtype import get_field_choices, get_field

class DynamicForm(models.Model):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def add_field_to_form(self, field):

        if field.form == self:
            return

        if self.fields.filter(name__iexact = field.name).count():
            raise ValueError("Field with the same name is already added to a form")

        field.form = self



    def __unicode__(self):
        return self.content_object.__unicode__()


class DynamicFormField(models.Model):
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, choices=get_field_choices())
    required = models.BooleanField(default=True)
    form = models.ForeignKey(DynamicForm, related_name='fields')
    additional_data = hstore.DictionaryField(blank=True, null=True)
    position = PositionField(collection='form')
    objects = hstore.HStoreManager()

    def get_django_field(self):
        return self.dynamic_field.load_field(self)

    @property
    def dynamic_field(self):
        return get_field(self.field_type)

    def __unicode__(self):
        return u'%s: %s' % (self.form.__unicode__(), self.name)


    class Meta:
        ordering = ['position']



class DynamicFormData(models.Model):
    form = models.ForeignKey(DynamicForm)
    user = models.ForeignKey(User)
    data = hstore.DictionaryField(db_index=True)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return u'%s %s' % (self.form, self.user)
