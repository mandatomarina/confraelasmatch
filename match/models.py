from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLE_CHOICES = (
    ('PACIENTE', 'Paciente'),
    ('PSICOLOGO', 'Psicologo'),
)

DAY_CHOICES = (
    (1, 'Domingo'),
    (2, 'Segunda'),
    (3, 'Terça'),
    (4, 'Quarta'),
    (5, 'Quinta'),
    (6, 'Sexta'),
    (7, 'Sabado')
)

# Create your models here.
class Horario(models.Model):
    weekday = models.IntegerField(default=2, choices=DAY_CHOICES)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return "{}: {} - {}".format(self.weekday, self.start, self.end)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='PACIENTE')
    nome = models.CharField(max_length=200)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.CharField(max_length=200, unique=True, blank=True, null=True, validators=[validate_email])

    def __str__(self):
        return self.nome

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  
    
class PsiProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    horario = models.ManyToManyField(Horario, related_name='horario_psiprofile', blank=True)
    registro = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.nome
    

class Atendimento(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paciente_atendimento')
    psicologo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psicologo_atendimento')
    horario = models.ManyToManyField(Horario, related_name='horario_paciente', blank=True)
    
    def __str__(self):
        return "{} > {}".format(self.medico.nome, self.paciente.nome)