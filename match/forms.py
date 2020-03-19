from django import forms
from django.forms import formset_factory
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
        fields = ('nome', 'phone', 'email')

class AtendimentoForm(forms.Form):
    horario = forms.TimeField(required=False)
    weekday = forms.ChoiceField(choices=DAY_CHOICES, required=False)

AtendimentoFormSet = formset_factory(AtendimentoForm, extra=3)