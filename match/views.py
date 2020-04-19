from django.shortcuts import render, redirect

# Create your views here.
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, AtendimentoForm
from .models import Profile, Horario


def home(request):
    return render(request, 'home.html')

def page(request, page_name):
    return render(request, 'pages/'+page_name+'.html')
   
def atendimento(request, edit=False):
    
    if request.method == 'POST':
        atendimento_form = AtendimentoForm(request.POST)
    
        livres = Profile.objects.filter(disponivel=True)
        if livres:
            return render(request, 'resultado.html', {
                'match' : livres.first(),
            })
    else:
        atendimento_form = AtendimentoForm()
    
    return render(request, 'atendimento.html', {
        'atendimento_form' : atendimento_form,
    })

@transaction.atomic
def signup(request):
    if request.user.is_authenticated:
        return redirect(atendimento)

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile = profile_form.save()
            user.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            redirect(home)

    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form' : profile_form
        })
