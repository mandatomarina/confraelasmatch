from .models import Event, Attendance
import datetime
from .utils import send_mail, msg_template
from django.conf import settings


WEEKDAY = {
  0 : 2,
  1 : 3,
  2 : 4,
  3 : 5,
  4 : 6,
  5 : 7,
  8 : 1  
}

def dailyreminder_job():
  weekday = datetime.datetime.today().weekday()
  events = Event.objects.filter(weekday=WEEKDAY[weekday])
  for event in events:
        attendance = Attendance.objects.filter(event=event.pk)
        for a in attendance:
            send_mail(
                '[Rede de Apoio] Lembrete! Você se inscreveu em '+event.kind.name,
                msg_template('confirmacao_psi.txt').format(name=a.attendee.first_name,kind=event.kind.name,weekday=event.day(),start=event.start,url=event.url),
                settings.EMAIL_HOST_USER,
                [a.attendee.email],
                fail_silently=False,
            )