from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.testlanding, name='testlanding'),
    path('portal/', views.livetestportalpage, name='livetestportalpage'),
]