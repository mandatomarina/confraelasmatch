from django.db import models
from django.contrib.auth.models import User


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
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'

    weekday = models.IntegerField(default=2, choices=DAY_CHOICES)
    start = models.TimeField()
    end = models.TimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    max_participants = models.IntegerField()
    kind = models.ForeignKey(Kind, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} - {} das {} - {}".format(self.kind, self.weekday, self.start, self.end)


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attedants')
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attending')
    is_attending = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.event, self.attendee)