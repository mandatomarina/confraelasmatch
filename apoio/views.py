from django.shortcuts import render
from .models import Kind

# Create your views here.
def KindList(request):
    kind = Kind.objects.all()
    context = { 'kind' : kind }
    return render(request, 'apoio/kindlist.html', context)