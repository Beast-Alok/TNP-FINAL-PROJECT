from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mentorhome, name='mentorhome'),
    path('take_test/', views.take_test, name='take_test'),
    path('view_test/', views.view_test, name='view_test'),
    path('mentor_announcements/', views.mentor_announcements, name='mentor_announcements'),
    path('info/', views.info, name='info'),
]