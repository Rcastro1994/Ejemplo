from django.shortcuts import render
from django.apps import apps
import pyodbc

def connection():
    s = '192.168.1.48' #47
    d = 'lnerp107' 
    u = 'sa'
    p = 'Pa$$w0rd'
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

def maestranza(request):
    maestranza = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT t_nmot, t_prot, t_nmsl, t_slct FROM tgvmae101201")
    for row in cursor.fetchall():
        maestranza.append({"nmot": row[0], "prot": row[1], "nmsl": row[2], "slct": row[3]})
    conn.close()
    return render(request, 'maestranza.html', {'maestranza':maestranza})
