from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('reject/<int:user_id>/', views.reject_user, name='reject_user'),
    path('mentor_invite/', views.mentor_invite, name='mentor_invite'),
]