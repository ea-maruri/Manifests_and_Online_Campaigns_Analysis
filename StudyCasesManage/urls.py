from django.urls import path

from StudyCasesManage import views

urlpatterns = [
  path('', views.home, name="Home"),
  path('conf/', views.configurator, name="Configurator"),
  path('cases-searcher/', views.cases_study_search, name="CasesSearcher"),
  path('search/', views.search_case, name="Search"),
  path('contact/', views.contact, name="Contact"),
]

