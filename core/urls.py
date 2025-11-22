#### FILE: core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('session/<int:session_id>/', views.interview, name='interview'),
    path('history/', views.history, name='history'),
]