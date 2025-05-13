from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.testlanding, name='testlanding'),
    path('active_test/', views.active_test, name='active_test'),
    path('start_test/', views.start_test, name='start_test'),
    path('portal/', views.livetestportalpage, name='livetestportalpage'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('check_test_started/<str:test_code>/', views.check_test_started, name='check_test_started'),
    path('end_test/', views.end_test, name='end_test'),
]