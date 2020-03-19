from django.shortcuts import render, redirect

# Create your views here.
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, AtendimentoFormSet
from .models import Profile


def home(request):
    return render(request, 'home.html')

@transaction.atomic
def signup(request):
    if request.user.is_authenticated:
        return redirect('/match/atendimento')

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form' : profile_form})

def atendimento(request):
    if not request.user.is_authenticated:
        return redirect('/match/signup')

    if request.method == 'POST':
        atendimento_form = AtendimentoFormSet(request.POST)
        if atendimento_form.is_valid():
            return render(request, 'resultado.html', {
                'data' : atendimento_form.cleaned_data,
            })

    else:
        atendimento_form = AtendimentoFormSet()
    return render(request, 'atendimento.html', {
        'atendimento_form' : atendimento_form
    })
    
    
