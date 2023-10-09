from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('consultar_lineas/', include('prueba.urls')), #Consultar Líneas de Orden de Venta
    #path('maestranza/', include('maestranza.urls')),
    path('', include('consultar_seguimiento.urls')), #Consultar Seguimiento Pedido 
    path('', include('cuenta_corriente.urls')) #Cuenta corriente   
]
