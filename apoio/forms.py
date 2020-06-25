from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile

class ApoioSignupForm(forms.Form):
    class Meta:
        model = User

    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    username = forms.HiddenInput()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']
        user.is_staff = True
        g1 = Group.objects.get(name='Usuário')
        user.groups.add(g1)
        user.save()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avaliable',)
        labels = {
            'avaliable': 'Disponível para novos atendimentos',
        }