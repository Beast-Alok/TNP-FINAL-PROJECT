from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_fun, name='login'),
    path('register/', views.register_fun, name='register'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('logout/', views.logout_fun, name='logout'),
]