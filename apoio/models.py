from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



DAY_CHOICES = (
    (1, 'Domingo'),
    (2, 'Segunda'),
    (3, 'Terça'),
    (4, 'Quarta'),
    (5, 'Quinta'),
    (6, 'Sexta'),
    (7, 'Sabado')
)

# Create your models here.

class Kind(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Event(models.Model):
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    weekday = models.IntegerField(default=2, choices=DAY_CHOICES, verbose_name=_('Weekday'))
    start = models.TimeField(verbose_name=_('Start'))
    end = models.TimeField(verbose_name=_('End'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Owner'))
    max_participants = models.IntegerField(verbose_name=_('Max Participants'))
    kind = models.ForeignKey(Kind, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Kind'))
    url = models.URLField(verbose_name=_('Meeting Link'), blank=True, null=True)

    def __str__(self):
        return "{}:{} - {} das {} - {}".format(self.kind, self.owner.first_name, DAY_CHOICES[self.weekday-1][1], self.start, self.end)


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attedants')
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attending')
    is_attending = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.event, self.attendee)