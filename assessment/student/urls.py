from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('view_mentor/', views.view_mentor, name='view_mentor'),
    path('history/', views.history, name='history'),
    path('announcement/', views.announcement, name='announcement'),
    path('community/', views.community, name='community'),
]