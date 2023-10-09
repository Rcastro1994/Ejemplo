from django.shortcuts import render
from django.apps import apps
import pyodbc
from datetime import datetime, date
from django.urls import reverse
from django.http import HttpResponseRedirect


def connection():
    s = '192.168.1.48' #47
    d = 'lnerp107' 
    #d = 'ln107gev' 
    u = 'sa'
    p = 'Pa$$w0rd'
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

def relacion_clientes(request):
    relacion = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute( '''
                    SELECT	
                    A.t_ofbp AS codigoPartner,
                    B.t_nama AS Cliente,
                    CASE
                        WHEN B.t_prst = '2' THEN 'Activo'
                        WHEN B.t_prst = '3' THEN 'Inactivo'
                        ELSE 'Cliente potencial'
                    END AS Estatus,
                    C.t_fovn AS RUC,
                    D.t_nama as Representante
                    FROM
                        ttccom110101 AS A,
                        ttccom100101 AS B,
                        ttctax400101 AS C,
                        ttccom001101 AS D
                    WHERE
                        A.t_crep = '52'
                        AND A.t_ofbp = B.t_bpid
                        AND A.t_ofbp = C.t_bpid
                        AND A.t_crep = D.t_emno''')
    for row in cursor.fetchall():
        relacion.append({"codigoPartner": row[0], "Cliente": row[1], "Estatus": row[2], "RUC": row[3], "Representante": row[4]})
    conn.close()
    return render(request, 'relacion_clientes.html', {
        'relacion':relacion
    })

def consultar_seguimiento(request, codigoPartner):
    seguimiento = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute( '''
                    SELECT                        	   
                    A.t_qono as Oferta, 
                    A.t_odat as FechaOferta, 
                    A.t_ohor as HoraOferta,                    
                    A.t_orno as OV_Numero, 
                    A.t_feco as FechaOrden, 
                    A.t_horo as HoraOrden,
                    A.t_fecb as FechaBloqueado, 
                    A.t_horb as HoraBloqueado, 
                    A.t_fecd as FechaDesbloqueado,
                    A.t_hord as HoraDesbloqueado,             
                    CONCAT(A.t_seri, '-' ,A.t_numi) as Factura,         
                    A.t_fecf as FechaFactura, 
	                A.t_horf as HoraFactura,                    
                    CONCAT(A.t_serg, '-', A.t_numg) as Guia,
                    A.t_fecg as FechaGuia, 
                    A.t_horg as HoraGuia,
                    A.t_bpid as Partner,
	                B.t_nama as NombrePartner
                    FROM tgvsls002101 as A, 
                        ttccom100101 as B 
                    WHERE A.t_bpid = ?
                    AND A.t_bpid = B.t_bpid''', (codigoPartner,))
    for row in cursor.fetchall():
        seguimiento.append({"Oferta": row[0], "FechaOferta": row[1], "HoraOferta": row[2], "OV_Numero": row[3], "FechaOrden": row[4],
                            "HoraOrden": row[5], "FechaBloqueado": row[6], "HoraBloqueado": row[7], "FechaDesbloqueado": row[8], "HoraDesbloqueado": row[9],
                            "Factura": row[10], "FechaFactura": row[11], "HoraFactura": row[12], "Guia": row[13], "FechaGuia": row[14], "HoraGuia": row[15], 
                            "Partner": row[16], "NombrePartner": row[17]})
    conn.close()
    return render(request, 'seguimiento.html', {
        'seguimiento':seguimiento,
        'codigoPartner':codigoPartner
    })