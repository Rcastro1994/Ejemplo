from django.shortcuts import render
from django.apps import apps
import pyodbc
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
import locale
import pandas as pd
from email.message import EmailMessage #CORREO ELECTRONICOS

def connection():
    s = '192.168.1.48' #47
    d = 'lnerp107' 
    #d = 'ln107gev' 
    u = 'sa'
    p = 'Pa$$w0rd'
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

def cuenta_corriente(request):    
    ccorriente = []
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
        ccorriente.append({"codigoPartner": row[0], "Cliente": row[1], "Estatus": row[2], "RUC": row[3], "Representante": row[4]})
    conn.close()
    return render(request, 'relacion_clientes_ccorriente.html', {
        'ccorriente':ccorriente        
    })

def seguimiento_ccorriente_cabecera(request, codigoPartner):
    #CABECERA
    seguimiento_ccorriente = []
    ccorriente_detalle = []
    conn = connection()

    cursor = conn.cursor()
    cursor.execute( '''
                    SELECT 
                        B.t_crep as Vendedor,
                        A.t_nama as NombreVendedor,
                        B.t_ofbp as Cliente,                         
                        C.t_nama as NombreCliente,	                         
                        D.t_ln02 as Direccion,                        
                        (G.t_dscr + ' ' + H.t_dscr + ' ' + I.t_dscr) as ln02,                        
                        E.t_fovn as RUC,	 
                        F.t_telm as Telefono,
                        F.t_fuln as RepresentanteLegal,
                        F.t_info as Correo
                    FROM 
                        ttccom001101 as A,
                        ttccom110101 as B,
                        ttccom100101 as C,
                        ttccom130101 as D,
                        ttctax400101 as E,
                        ttccom140101 as F,
                        tgvfel013101 as G,
                        tgvfel096101 as H,
                        tgvfel097101 as I                        
                    WHERE                          
                        B.t_ofbp = ?                        
                        AND A.t_emno = B.t_crep
                        AND B.t_ofbp = C.t_bpid
                        AND C.t_cadr = D.t_cadr
                        AND C.t_bpid = E.t_bpid
                        AND C.t_ccnt = F.t_ccnt
                        AND G.t_dstr = D.t_ccit
                        AND H.t_prvn = G.t_prvn
                        AND I.t_dprt = G.t_dprt''', (codigoPartner,))
    for row in cursor.fetchall():
        seguimiento_ccorriente.append({"Vendedor": row[0], "NombreVendedor": row[1], "Cliente": row[2], "NombreCliente": row[3], "Direccion": row[4], "ln02": row[5], 
                                       "RUC": row[6],"Telefono":row[7], "RepresentanteLegal":row[8], "Correo":row[9]})
    #cursor.fetchone
    cursor.close()

    #DETALLE
    cursord = conn.cursor()
    cursord.execute('''
                    SELECT 
                        A.t_ccur as Moneda,  
                        (SELECT E.t_glosa from tgvcmg006101 as E WHERE E.t_ninv = A.t_ninv AND E.t_ttyp = A.t_ttyp) as Banco,                       
                        CONCAT(A.t_ttyp, '-' , A.t_ninv) as Documento,                        
                        A.t_orno as Orden,
                        A.t_docd as FechaEmision,
                        A.t_dued as FechaVencimiento,
                        (SELECT E.t_nmro from tgvcmg006101 as E WHERE E.t_ninv = A.t_ninv AND E.t_ttyp = A.t_ttyp) as Cod_Unico,
                        A.t_balh_2 as Saldo,
                        (SELECT CASE E.t_stat
                                    WHEN '5' THEN 'Cartera No Aceptada' 
                                    WHEN '6' THEN 'En Cartera' 
                                    WHEN '7' THEN 'Descuento No Abonada'	
                                    WHEN '8' THEN 'Descuento'
                                    WHEN '9' THEN 'Cobranza No Abonada'
                                    WHEN '10' THEN 'Cobranza'
                                    WHEN '11' THEN 'Protestada'
                                    WHEN '12' THEN 'Cancelada'
                                    WHEN '13' THEN 'No Portestada'				
                                    ELSE 'Cartera' END			
                                    FROM tgvcmg006101 as E 
                        WHERE E.t_ninv = A.t_ninv AND E.t_ttyp = A.t_ttyp) as Estado,
                        D.t_crlr as Credito
                        FROM   
                            ttfacr200101 as A,	 
                            ttccom110101 as B,	 	   
                            ttccom100101 as C,
                            ttccom112101 as D
                        WHERE  A.t_itbp = B.t_ofbp
                            AND A.t_crep = B.t_crep	
                            AND B.t_ofbp = C.t_bpid     
                            AND C.t_bpid = D.t_itbp                    
                            AND B.t_ofbp = ?
                            AND A.t_docn = 0
                            AND (A.t_balc <> 0 OR A.t_balh_2 <> 0)
                            AND D.t_crlr > 0
                        ORDER BY A.t_ttyp''', (codigoPartner,))
    for row in cursord.fetchall():
        ccorriente_detalle.append({"Moneda": row[0], "Banco": row[1], "Documento": row[2], "Orden": row[3], "FechaEmision": row[4], "FechaVencimiento": row[5], "Cod_Unico": row[6], "Saldo": row[7], "Estado": row[8], "Credito": row[9]})
    cursord.close
    conn.close()         
    
    #Obtener Dia, Mes, Año & Colocar Mes en Español con locale
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')    
    fecha_actual = datetime.now()    
    fecha_formateada = fecha_actual.strftime("%d DE %B DE %Y")    
    locale.setlocale(locale.LC_TIME, '')
    fecha_formateada = fecha_formateada.upper()

    #Obtener la fecha y hora actual
    fecha_hora = datetime.now()    
    fecha_formateada1 = fecha_hora.strftime("%d.%m.%Y")    
    hora_formateada = fecha_hora.strftime("- %H:%M")    
    fecha_hora_formateada = fecha_formateada1 + " " + hora_formateada    

    #Suma Total de Saldo
    total_saldo = sum(consulta['Saldo'] for consulta in ccorriente_detalle)


    return render(request, 'seguimiento_ccorriente.html', {
        'fecha_actual': fecha_formateada,
        'fecha_hora':fecha_hora_formateada,
        'seguimiento_ccorriente':seguimiento_ccorriente,        
        'ccorriente_detalle':ccorriente_detalle,     
        'codigoPartner':codigoPartner,
        'total_saldo': total_saldo
    })