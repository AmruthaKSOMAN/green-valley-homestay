
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    # Public Website
    path('', views.home, name='home'),

    # Owner Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

]
