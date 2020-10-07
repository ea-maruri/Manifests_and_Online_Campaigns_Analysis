from os import name
from django.urls import path

from StudyCasesManage import views

urlpatterns = [
  path('', views.home, name="home"),
  path('conf/', views.configurator, name="configurator"),
  path('cases-searcher/', views.cases_study_search, name="cases_searcher"),
  path('search/', views.search_case, name="search"),
  path('contact/', views.contact, name="contact"),
  path('login/', views.login, name="login"),
  path('register/', views.register, name="register"),
]

