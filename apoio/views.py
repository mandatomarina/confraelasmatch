from django.shortcuts import render, HttpResponse
from .models import Kind, Attendance
from .forms import ProfileForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from saudemental import settings

# Create your views here.
def KindList(request):
    #return HttpResponse(settings.LOCALE_PATHS)

    kind = Kind.objects.all()
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Seu perfil foi salvo corretamente.'))
            #return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    
    events = Attendance.objects.filter(attendee=request.user)
    return render(request, 'apoio/kindlist.html', {
        'profile_form': profile_form,
        'kind' : kind,
    })

def ProfileView(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            #return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    
    events = Attendance.objects.filter(attendee=request.user)
    return render(request, 'apoio/profile.html', {
        'profile_form': profile_form,
        'events' : events,
    })