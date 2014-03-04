# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from softdelete.models import SoftDeleteObject
from categories.models import CategoryBase
from categories.settings import THUMBNAIL_UPLOAD_PATH


class AttractionCategory(CategoryBase):
    thumbnail = models.ImageField(
        upload_to=THUMBNAIL_UPLOAD_PATH,
        null=True, blank=True)

    class Meta:
        verbose_name_plural = 'attraction categories'

    def __str__(self):
        if self.parent:
            return "<AttractionCategory, '{}/{}'>".format(
                self.parent.name, self.name)
        else:
            return "<AttractionCategory, '{}'>".format(self.name)


class SportCategory(AttractionCategory):

    class Meta:
        verbose_name_plural = 'sport categories'


class Organizer(models.Model):
    name = models.CharField(_("name"), max_length=200)
    mail = models.EmailField(_("e-mail address"))
    phone = models.CharField(_("phone number"), max_length=20)
    address = models.TextField(_("address"), blank=True, null=True)
    related_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class SerialEventGroup(models.Model):
    name = models.CharField(_("name"), max_length=200)

    def __unicode__(self):
        return self.name


class Event(SoftDeleteObject):
    name = models.CharField(_("event name"), max_length=200,
                            help_text=_("Without edition (eg. \"Long Race\", "
                                        "not \"Long Race 2013\")"))
    start_date = models.DateTimeField(_("start date of the event"),
                                      null=True, blank=True)
    end_date = models.DateTimeField(_("end date of the event"),
                                    null=True, blank=True)
    logo = models.ImageField(upload_to='uploads/events/logos',
                             null=True, blank=True)
    website = models.URLField(_("website"), max_length=100, blank=True)
    created_by = models.ForeignKey(User)
    category = models.ForeignKey(SportCategory,
                                 verbose_name=_('category'))
    description = models.TextField(_("description of the event"),
                                   blank=True, null=True)
    organizer = models.ForeignKey(Organizer)
    edition = models.CharField(_("edition name"), max_length=100,
                               blank=True,
                               help_text=_("Only if event is cyclic (eg. "
                                           "\"1\", \"2014\")"))
    event_group = models.ForeignKey(SerialEventGroup, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_logo(self):
        return self.logo if self.logo else self.category.thumbnail

    def get_other_editions(self):
        if self.event_group:
            return self.event_group.event_set.all().exclude(edition=
                                                            self.edition)


class Attraction(SoftDeleteObject):
    event = models.ForeignKey(Event)
    name = models.CharField(_("name"), max_length=200)
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    logo = models.ImageField(upload_to='uploads/events/logos',
                             null=True, blank=True)
    place = models.CharField(_("place"), max_length=200)
    description = models.TextField(
        _("description of the attraction"), null=True, blank=True)
    category = models.ForeignKey(AttractionCategory,
                                 verbose_name=
                                 _('category'))

    def __unicode__(self):
        return self.name

    def get_logo(self):
        return self.logo if self.logo else self.category.thumbnail

    class Meta:
        ordering = ['start_date', 'name']
