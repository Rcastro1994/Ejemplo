from django.urls import path
from . import views

app_name = 'cuenta_corriente'

urlpatterns = [           
    path('relacion_clientes_ccorriente/', views.cuenta_corriente, name='cuenta_corriente'),     
    path('seguimiento_ccorriente/<str:codigoPartner>', views.seguimiento_ccorriente_cabecera, name='seguimiento_ccorriente_cabecera')
    #path('seguimiento_ccorriente/<str:codigoPartner>', views.seguimiento_ccorriente_detalle, name='seguimiento_ccorriente_detalle')
]