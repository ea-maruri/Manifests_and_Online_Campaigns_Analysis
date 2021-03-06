"""Manifests_and_Online_Campaigns_Analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static  # to use media and static files
from . import views
# Import App

urlpatterns = [
  path('admin/', admin.site.urls),
  path('StudyCasesManage/', include('StudyCasesManage.urls')),
  path('Configurator/', include('StudyCasesConfApp.urls')),
  path('accounts/', include('django.contrib.auth.urls')),  # Use django auth (login, logout, etc)
  path('edit-profile/', views.edit_profile, name='edit_profile')
]

#if settings.DEBUG: ??
# In order to use static urls (for media like images or PDFs)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
