from django.urls import path
from . import views


app_name = 'maestranza'

urlpatterns = [    
    path('', views.maestranza, name='maestranza')
    
]