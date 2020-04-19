from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    nome = models.CharField(max_length=200)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.CharField(max_length=200, unique=True, blank=True, null=True, validators=[validate_email])
    horario = models.ManyToManyField(Horario, related_name='horario_profile', blank=True)
    registro = models.CharField(max_length=20, unique=True, blank=True, null=True)
    disponivel = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Atendimento(models.Model):
    paciente = models.CharField(max_length=200)
    autorizacao = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()