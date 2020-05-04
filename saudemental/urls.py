"""saudemental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
from .views import home, page
from apoio.admin import myadmin

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/accounts/login/?next=/admin/apoio/list', permanent=False)),
    path('page/<slug:page_name>', page),
    path('admin/', myadmin.urls),
    path('accounts/', include('allauth.urls')),
]
