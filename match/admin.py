from django.contrib import admin
from .models import Profile, PsiProfile, Atendimento, Horario
# Register your models here.


admin.site.register(Profile)
admin.site.register(PsiProfile)
admin.site.register(Atendimento)
admin.site.register(Horario)