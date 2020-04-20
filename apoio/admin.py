from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from .models import Event, Attendance, Kind
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect



class MyAdminSite(admin.AdminSite):
    site_header = 'Rede de Apoio aos Psicologos'

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'owner',
        'get_participants',
        'events_actions' 
    )

    list_filter = (
        'kind',
    )
     
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

    get_participants.short_description = "Participantes"

    def events_actions(self, obj):
        if not Attendance.objects.filter(event=obj.pk, attendee=self.request.user.id):
            return format_html(
                '<a class="button" href="{}?next={}">Join</a>&nbsp;',
                reverse('admin:join-event', args=[obj.pk]),
                self.request.path
            )
        else:
            return format_html('<a class="button" href="{}?next={}">Leave</a>',
                reverse('admin:leave-event', args=[obj.pk]),
                self.request.path)
            
               
    events_actions.short_description = 'Actions'
    events_actions.allow_tags = True

    def join_event(self, request, event_id, *args, **kwargs):
        next = request.GET.get('next', '/default/url/')
        event = Event.objects.get(pk=event_id)
        if Attendance.objects.filter(event=event_id).count() < event.max_participants and not Attendance.objects.filter(event=event_id, attendee=request.user.id):
            a = Attendance(event=Event.objects.get(pk=event_id), attendee=User.objects.get(pk=request.user.id), is_attending=True)
            a.save()
            messages.success(request, 'Você foi inscrito no evento com sucesso!')
            return redirect(next)
        else:
            return redirect(next)
        
    def leave_event(self, request, event_id, *args, **kwargs):
        next = request.GET.get('next', '/default/url/')
        a = Attendance.objects.filter(event=event_id, attendee=request.user.id)
        if a:
            a.delete()
            messages.success(request, 'Você não esta mais participando do evento.')
            return redirect(next)
        else:
            return redirect(next)

myadmin = MyAdminSite(name="myadmin")

myadmin.register(Event, EventAdmin)
admin.site.register(Attendance)
admin.site.register(Kind)
