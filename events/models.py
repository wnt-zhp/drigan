from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Event(models.Model):
    event_name = models.CharField(_("name of the event"), max_length=200)
    event_start_date = models.DateTimeField(_("start date of the event"))
    event_end_date = models.DateTimeField(_("end date of the event"))
    event_website = models.CharField(_("website"), max_length=100, null=True, blank=True)
    organizer = models.ForeignKey(User)
    categories = models.ManyToManyField('categories.Category', verbose_name = _('categories'))
    def __unicode__(self):
        return self.event_name
