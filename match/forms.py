from django import forms
from .models import Profile, Atendimento

DAY_CHOICES = (
    (1, 'Domingo'),
    (2, 'Segunda'),
    (3, 'Terça'),
    (4, 'Quarta'),
    (5, 'Quinta'),
    (6, 'Sexta'),
    (7, 'Sabado')
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ()

class AtendimentoForm(forms.ModelForm):
    
    class Meta:
        model = Atendimento
        exclude = ()