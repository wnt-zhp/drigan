from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Event(models.Model):
    event_name = models.CharField(_("name"), max_length=200)
    event_start_date = models.DateTimeField(_("start date of the event"))
    event_end_date = models.DateTimeField(_("end date of the event"))
    event_website = models.CharField(_("website"), max_length=100,
                                     null=True, blank=True)
    created_by = models.ForeignKey(User)
    categories = models.ManyToManyField('categories.Category',
                                        verbose_name=_('categories'))
    event_description = models.TextField(_("description of the event"),
                                         blank=True, null=True)

    def __unicode__(self):
        return self.event_name


class Attraction(models.Model):
    event = models.ForeignKey(Event)
    attraction_name = models.CharField(_("name"), max_length=200)
    attraction_start_date = models.DateTimeField(_("start date"))
    attraction_end_date = models.DateTimeField(_("end date"))
    attraction_place = models.CharField(_("place"), max_length=200)
    attraction_description = models.TextField(
        _("description of the attraction"), null=True, blank=True)
    attraction_categories = models.ManyToManyField('categories.Category',
                                                   verbose_name=
                                                   _('categories'))

    def __unicode__(self):
        return self.attraction_name


class Organizer(models.Model):
    organizer_name = models.CharField(_("name"), max_length=200)
    organizer_mail = models.EmailField(_("e-mail address"))
    organizer_phone = models.CharField(_("phone number"), max_length=20)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.organizer_name
