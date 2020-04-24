from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from .models import Event, Attendance, Kind
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django import forms
from django.conf.urls import url
from .views import KindList


DEFAULT_SEND_MAIL = "pedro@markun.com.br"
TEMPLATE_MESSAGE = """Olá {}, você esta inscrito em {}."""

class MyAdminSite(admin.AdminSite):
    site_header = _('Rede de Apoio aos Psicologos')

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        custom_urls = [
            url(r'apoio/list/', self.admin_view(KindList), name="apoio_kind_list"),
        ]
        return urls + custom_urls


# Register your models here.

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner']

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'kind',
        'weekday',
        'start',
        'owner',
        'get_participants',
        'events_actions' 
    )

    list_filter = (
        'kind',
    )

    form = EventForm
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        self.request = request
        return qs
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<event_id>/join/',
                self.admin_site.admin_view(self.join_event),
                name='join-event',
            ),
            path(
                '<event_id>/leave/',
                self.admin_site.admin_view(self.leave_event),
                name='leave-event',
            ),
        ]
        return custom_urls + urls
    
    def get_participants(self, obj):
        return "{}/{}".format(Attendance.objects.filter(event=obj.pk).count(),obj.max_participants)

    get_participants.short_description = _("Participants")

    def events_actions(self, obj):
        if not Attendance.objects.filter(event=obj.pk, attendee=self.request.user.id):
            return format_html(
                '<a class="button" href="{}?next={}">{}</a>&nbsp;',
                reverse('admin:join-event', args=[obj.pk]),
                self.request.path,
                _('Join')
            )
        else:
            return format_html('<a class="button" href="{}?next={}">{}</a>',
                reverse('admin:leave-event', args=[obj.pk]),
                self.request.path,
                _('Leave'))
            
               
    events_actions.short_description = _('Actions')
    events_actions.allow_tags = True

    def join_event(self, request, event_id, *args, **kwargs):
        next = request.GET.get('next', '/default/url/')
        event = Event.objects.get(pk=event_id)
        if Attendance.objects.filter(event=event_id).count() < event.max_participants and not Attendance.objects.filter(event=event_id, attendee=request.user.id):
            a = Attendance(event=Event.objects.get(pk=event_id), attendee=User.objects.get(pk=request.user.id), is_attending=True)
            name = a.__str__()
            a.save()
            
            send_mail(
                '[Rede de Apoio] Você se inscreveu em '+name,
                TEMPLATE_MESSAGE.format(request.user.first_name, name),
                DEFAULT_SEND_MAIL,
                [request.user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'You have joined '+name)
            return redirect(next)
        else:
            return redirect(next)
        
    def leave_event(self, request, event_id, *args, **kwargs):
        next = request.GET.get('next', '/default/url/')
        a = Attendance.objects.filter(event=event_id, attendee=request.user.id)
        if a:
            name = a[0].__str__()
            a.delete()
            messages.success(request, _('You have left '+name))
            return redirect(next)
        else:
            return redirect(next)

myadmin = MyAdminSite(name="myadmin")

myadmin.register(Event, EventAdmin)
myadmin.register(Attendance)
myadmin.register(Kind)
myadmin.register(User)
myadmin.register(Group)
