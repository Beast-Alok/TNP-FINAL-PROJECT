from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mentorhome, name='mentorhome'),
    path('make_test_next/', views.make_test_next, name='make_test_next'),
    path('take_test/', views.take_test, name='take_test'),
    path('view_test/', views.view_test, name='view_test'),
    path('mentor_announcements/', views.mentor_announcements, name='mentor_announcements'),
    path('save_questions/', views.save_questions, name='save_questions'),
    path('info/', views.info, name='info'),
]