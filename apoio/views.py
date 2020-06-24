from django.shortcuts import render
from .models import Kind, Attendance

# Create your views here.
def KindList(request):
    kind = Kind.objects.all()
    context = { 'kind' : kind }
    return render(request, 'apoio/kindlist.html', context)

def Profile(request):
    events = Attendance.objects.filter(attendee=request.user)
    context = { 'events' : events }
    return render(request, 'apoio/profile.html', context)