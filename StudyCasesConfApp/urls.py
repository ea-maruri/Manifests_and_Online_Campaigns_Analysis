from django.urls import path

# Import views
from . import views

urlpatterns = [
  path('', views.configurator, name="configurator"),
]
