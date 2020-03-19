from django.conf.urls import url
from match import views as core_views

urlpatterns = [
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^atendimento/$', core_views.atendimento, name='atendimento')
]