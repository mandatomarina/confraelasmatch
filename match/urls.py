from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from match import views as core_views


urlpatterns = [
    path('atendimento/', core_views.atendimento, name='atendimento'),
    path('signup/', core_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
]