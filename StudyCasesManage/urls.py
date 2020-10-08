from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import views
from StudyCasesManage import views

urlpatterns = [
  path('', views.home, name="home"),
  path('cases-searcher/', views.cases_study_search, name="cases_searcher"),
  path('search/', views.search_case, name="search"),
  path('contact/', views.contact, name="contact"),
  path('login/', views.login, name="login"),
  path('register/', views.register, name="register"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
