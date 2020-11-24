from StudyCasesConfApp.views import case_study_conf, data_collection_conf
from django.urls import path

# Import views
from . import views

urlpatterns = [
  path('', views.configurator, name="configurator"),
  path('case-study-conf/', views.case_study_conf, name="case_study_conf"),
  path('data-collection-conf/', views.data_collection_conf, name="data_collect_conf"),
  path('case-study-conf/', views.case_study_conf, name="case_conf"),
  path('analysis-conf/', views.analysis_conf, name="analysis_conf"),
  # path('document-conf/', views.document_conf, name="doc_conf"),
]
