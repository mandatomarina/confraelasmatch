from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from .models import Event, Attendance, Kind
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf.urls import url
from .views import KindList
from .utils import send_mail, msg_template
from django.conf import settings


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
        exclude = []

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'kind',
        'weekday',
        'start',
        'owner',
        'get_participants',
        'events_actions'
    )

    ordering = ('kind','weekday','start')

    list_filter = (
        'kind',
    )

    list_display_links = None

    form = EventForm
    
    change_form_template = 'apoio/change_event_form.html'


    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.owner:
            return True
        else:
            return super(EventAdmin, self).has_change_permission(request, obj)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['atendee'] = self.get_participants_list(object_id)
        return super(EventAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        self.request = request
        return qs

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('owner')

        return super(EventAdmin, self).get_form(request, obj, **kwargs)
    
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
            path(
                '<event_id>/remove_all/',
                self.admin_site.admin_view(self.remove_all),
                name='remove-all',
            ),
        ]
        return custom_urls + urls
    
    def get_participants(self, obj):
        return "{}/{}".format(Attendance.objects.filter(event=obj.pk).count(),obj.max_participants)

    def get_participants_list(self, object_id):
        return Attendance.objects.filter(event=object_id)

    get_participants.short_description = _("Participants")
    
    def events_actions(self, obj):
        btn = None
        if Event.objects.get(pk=obj.pk).owner == self.request.user:
            btn = format_html('  <a class="button" href="{}">{}</a>',
            reverse('admin:%s_%s_change' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.id] ),
                _('Edit'))
            btn += format_html('  <a class="button" href="{}?next={}">{}</a>',
            reverse('admin:remove-all', args=[obj.id]),
                self.request.path,
                _('Remover participantes'))
        elif Attendance.objects.filter(event=obj.pk, attendee=self.request.user.id):
            btn = format_html('<a class="button" href="{}?next={}">{}</a>',
                reverse('admin:leave-event', args=[obj.pk]),
                self.request.path,
                _('Leave'))
            if (obj.url):
                btn += format_html(' <a class="button" href="{}" target="_blank">{}</a>',
                    obj.url,
                    _('Link'))
        elif Attendance.objects.filter(event=obj.pk).count() >= Event.objects.get(pk=obj.pk).max_participants:
            btn = format_html('<a class="button" href="#">Evento cheio</a>')
        else:
            btn = format_html(
                '<a class="button" href="{}?next={}">{}</a>&nbsp;',
                reverse('admin:join-event', args=[obj.pk]),
                reverse('admin:%s_%s_change' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.id] ),
                _('Join')
            )
        return btn
    events_actions.short_description = _('Actions')
    events_actions.allow_tags = True

    def join_event(self, request, event_id, *args, **kwargs):
        n = request.GET.get('next', '/default/url/')
        event = Event.objects.get(pk=event_id)
        if Attendance.objects.filter(event=event_id).count() < event.max_participants and not Attendance.objects.filter(event=event_id, attendee=request.user.id):
            a = Attendance(event=event, attendee=request.user, is_attending=True)
            name = a.__str__()
            a.save()
            
            send_mail(
                '[Rede de Apoio] Você se inscreveu em '+event.kind.name,
                msg_template('confirmacao_psi.txt').format(name=request.user.first_name,kind=event.kind.name,weekday=event.day(),start=event.start,url=event.url),
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            
            send_mail(
                '[Rede de Apoio] '+request.user.first_name+ ' se inscreveu em '+event.kind.name,
                msg_template('confirmacao_coord.txt').format(name=request.user.first_name,kind=event.kind.name,weekday=event.day(),start=event.start,url=event.url),
                settings.EMAIL_HOST_USER,
                [event.owner.email],
                fail_silently=False,
            )

            messages.success(request, 'You have joined '+name)
            return redirect(n)
        else:
            return redirect(n)
        
    def leave_event(self, request, event_id, *args, **kwargs):
        n = request.GET.get('next', '/default/url/')
        a = Attendance.objects.filter(event=event_id, attendee=request.user.id)
        if a:
            name = a[0].__str__()
            a.delete()
            messages.success(request, _('You have left '+name))
            return redirect(n)
        else:
            return redirect(n)
    
    def remove_all(self, request, event_id, *args, **kwargs):
        n = request.GET.get('next', '/default/url/')
        a = Attendance.objects.filter(event=event_id)
        count = a.count()
        a.delete()
        messages.success(request, _('Você removeu '+ str(count)+' participantes.'))
        return redirect(n)


myadmin = MyAdminSite(name="myadmin")

myadmin.register(Event, EventAdmin)
myadmin.register(Attendance)
myadmin.register(Kind)
myadmin.register(User)
myadmin.register(Group)
myadmin.register(Site)
