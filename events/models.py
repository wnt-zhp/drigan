from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Organizer(models.Model):
    name = models.CharField(_("name"), max_length=200)
    mail = models.EmailField(_("e-mail address"))
    phone = models.CharField(_("phone number"), max_length=20)
    address = models.TextField(_("address"), blank=True, null=True)
    related_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(_("event name"), max_length=200)
    start_date = models.DateTimeField(_("start date of the event"),
                                      null=True, blank=True)
    end_date = models.DateTimeField(_("end date of the event"),
                                    null=True, blank=True)
    website = models.CharField(_("website"), max_length=100, blank=True)
    created_by = models.ForeignKey(User)
    category = models.ForeignKey('categories.Category',
                                 verbose_name=_('category'),
                                 null=True, blank=True)
    description = models.TextField(_("description of the event"), blank=True)
    organizer = models.ForeignKey(Organizer)

    def __unicode__(self):
        return self.name


class Attraction(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(_("name"), max_length=200)
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    place = models.CharField(_("place"), max_length=200)
    description = models.TextField(
        _("description of the attraction"), null=True, blank=True)
    category = models.ForeignKey('categories.Category',
                                 verbose_name=
                                 _('category'))

    def __unicode__(self):
        return self.name
