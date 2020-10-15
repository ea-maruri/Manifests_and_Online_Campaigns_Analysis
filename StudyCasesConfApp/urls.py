from os import name
from django.urls import path

# Import views
from . import views

urlpatterns = [
  path('', views.configurator, name="configurator"),
  path('case-study-conf/', views.case_study_conf, name="case_study_conf"),
  path('data-collection-conf/', views.data_collection_conf, name="data_collect_conf"),
  path('upload-file', views.upload_file, name="upload_file"),
]
