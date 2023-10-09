from django.urls import path
from . import views

app_name = 'consultar_seguimiento'

urlpatterns = [    
    #Bien
    #path('seguimiento/<str:codigoPartner>', views.consultar_seguimiento, name='consultar_seguimiento'),
    #path('', views.relacion_clientes, name='relacion_clientes')  

    path('relacion_clientes/', views.relacion_clientes, name='relacion_clientes'),
    path('seguimiento/<str:codigoPartner>', views.consultar_seguimiento, name='consultar_seguimiento')    
     
]