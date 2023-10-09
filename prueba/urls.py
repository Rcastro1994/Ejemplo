from django.urls import path
from . import views

app_name = 'prueba'

urlpatterns = [
    path('', views.consultar, name='consultar'),    
]