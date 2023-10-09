from django.shortcuts import render
from django.apps import apps
import pyodbc

def connection():
    s = '192.168.1.48' #47
    d = 'lnerp107' 
    #d = 'ln107gev' 
    u = 'sa'
    p = 'Pa$$w0rd'
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn


#def pagina(request):
#    ordenes = []
#    conn = connection()
#    cursor = conn.cursor()
#    cursor.execute("SELECT A.t_orno, A.t_ofbp, A.t_ofad, A.t_stbp FROM ttdsls400201 as A")
#    for row in cursor.fetchall():
#        ordenes.append({"orno": row[0], "ofbp": row[1], "ofad": row[2], "stbp": row[3]})
#    conn.close()
#    return render(request, 'pagina.html', {'ordenes':ordenes})

def consultar(request):
    ordenes = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute( '''select A.t_orno as OrdenVenta,
	                  A.t_pono as Linea,
	                  A.t_oref as Referencia,
	                  CONCAT(A.t_ofbp,' - ', B.t_nama) as Partner,
	                  A.t_bkyn as Bloqueado,	   	 
	                  CONCAT(trim(A.t_item),' - ', C.t_dsca) as Item,
	                  CONCAT(A.t_qoor,'  ', A.t_cuqs) as CantidadPedida,	   
	                  CONCAT(A.t_qidl,'  ', C.t_cuni) as CantidadEntregada,
	                  A.t_pric as Precio,	   
	                  CONCAT(A.t_disc_1,'  -  ', A.t_disc_2,'  -  ',A.t_disc_3) as Descuentos,
	                  D.t_odis as DescuentoOrden,
	                  A.t_odat as FechaFactura,	  
	                  CONCAT(A.t_ttyp, ' - ', A.t_invn) as Factura
                      from ttdsls401101 as A,
                   	       ttccom100101 as B,
	                       ttcibd001101 as C,
	                       ttdsls400101 as D
                      where A.t_ofbp = B.t_bpid 
	                  and A.t_item = C.t_item
	                  and A.t_orno = D.t_orno
	                  and D.t_crep = '205'
                      order by A.t_orno''')
    for row in cursor.fetchall():
        ordenes.append({"OrdenVenta": row[0], "Linea": row[1], "Referencia": row[2], "Partner": row[3], "Bloqueado": row[4],
                        "Item": row[5], "CantidadPedida": row[6], "CantidadEntregada": row[7], "Precio": row[8], "Descuentos": row[9],
                        "DescuentoOrden": row[10], "FechaFactura": row[11], "Factura": row[12]})
    conn.close()
    return render(request, 'pagina.html', {'ordenes':ordenes})

