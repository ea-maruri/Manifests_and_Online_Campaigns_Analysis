from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import views
from StudyCasesManage import views

urlpatterns = [
  path('', views.home, name="home"),
  path('contact/', views.contact, name="contact"),
  path('login/', views.login, name="login"),
  path('register/', views.register, name="register"),
  path('posts/', views.TableListView.as_view(), name="posts")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
