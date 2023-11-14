from datetime import datetime, timedelta
from db.conection import DatabaseConnection

# def dias_del_mes_bimestre():
#     dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]    
#     meses_bimestre = bimestre_actual()
#     dias_bimestre = [dias_por_mes[mes] for mes in meses_bimestre]    
#     return dias_bimestre

def bimestre_actual():
    mes_actual = datetime.now().month
    bimestre = (mes_actual - 1) // 2 + 1
    mes_inicial = (bimestre - 1) * 2 + 1
    mes_final = bimestre * 2 + 1
    return list(range(mes_inicial, mes_final))


def cantidad_dias(fecha1, fecha2, mes):
    fecha1 = datetime.strptime(fecha1, '%Y-%m-%d')
    fecha2 = datetime.strptime(fecha2, '%Y-%m-%d')
    if fecha1.month == fecha2.month == mes:
        diferencia = abs((fecha2 - fecha1).days)
        return diferencia+1
    elif fecha1.month == mes:
        ultimo_dia_mes = (fecha1 + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        dias_hasta_final_mes = (ultimo_dia_mes - fecha1).days
        return dias_hasta_final_mes+1
    elif fecha2.month == mes:
        primer_dia_mes = datetime(fecha2.year, mes, 1)
        dias_desde_inicio_mes = (fecha2 - primer_dia_mes).days
        return dias_desde_inicio_mes+1
    else:
        return 0     
     
      

def prueba(legajo):
    meta_q = 0
    meta_monto = 0
    progresiones = 0
    mes_uno = 0
    mes_dos = 0
    tutoria = 0
    licencia_especial = 0
    bimestre = bimestre_actual()
    
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()    
    
    nomina_query = "SELECT * FROM tec_nominaAllDataVM WHERE employeeNumber = ?"
    cursor.execute(nomina_query, legajo)
    rows_nomina = cursor.fetchall()
    
    progresion_query = "SELECT * FROM tec_progretionOfUsers WHERE employeeNumber = ?"
    cursor.execute(progresion_query, legajo)
    rows_progresiones = cursor.fetchall()
    
    licencia_query = "SELECT startDay, endDay FROM tec_licencesReports WHERE employeeNumber = ?"
    cursor.execute(licencia_query, legajo)
    rows_licencia = cursor.fetchall()
    
    tutores_query = "SELECT * FROM tec_tutoresVM WHERE employeeNumber = ?"
    cursor.execute(tutores_query, legajo)
    rows_tutores = cursor.fetchall()    
    
    licencia_special_query = "SELECT * FROM tec_licencesSpecialReports WHERE employeeNumber = ?"
    cursor.execute(licencia_special_query, legajo)
    rows_licencia_especial = cursor.fetchall()
    
    for row_nomina in rows_nomina:
        metas_q = row_nomina[6]
        metas_monto = row_nomina[7]
        meta_q += metas_q
        meta_monto += metas_monto
        
    for row_progress in rows_progresiones:
        ajuste_progress = row_progress[4]
        progresiones += ajuste_progress
        
    for row_licencia in rows_licencia:
        fecha_desde = row_licencia[0]
        fecha_hasta = row_licencia[1]
        mes_uno += cantidad_dias(str(fecha_desde), str(fecha_hasta), bimestre[0])
        mes_dos += cantidad_dias(str(fecha_desde), str(fecha_hasta), bimestre[1])
    if mes_uno >= 7 and mes_uno <= 21:
        mes_uno = mes_uno*0.01
    else:
        mes_uno = 0
    if mes_dos >= 7 and  mes_dos <= 21:
        mes_dos = mes_dos*0.01
    else:
        mes_dos = 0
        
    for row_tutor in rows_tutores:
        ajuste = row_tutor[6]
        tutoria += ajuste        
        
    for rows_licen_esp in rows_licencia_especial:
        ajuste_lic_esp = rows_licen_esp[7]
        licencia_especial += ajuste_lic_esp
        
    
    total_licencias = mes_uno + mes_dos
    valor_maximo = max(total_licencias, tutoria, licencia_especial)
    if valor_maximo == total_licencias:
        segundo_mayor = max(tutoria, licencia_especial)
        minimo = min(tutoria, licencia_especial)
    elif valor_maximo == tutoria:
        segundo_mayor = max(total_licencias, licencia_especial)
        minimo = min(total_licencias, licencia_especial)
    else:
        segundo_mayor = max(total_licencias, tutoria)
        minimo = min(total_licencias, tutoria)
        
    valor_maximo_q_uno = max(mes_uno, tutoria, licencia_especial)
    if valor_maximo_q_uno == mes_uno:
        segundo_mayor_q_uno = max(tutoria, licencia_especial)
        minimo_q_uno = min(tutoria, licencia_especial)
    elif valor_maximo_q_uno == tutoria:
        segundo_mayor_q_uno = max(mes_uno, licencia_especial)
        minimo_q_uno = min(mes_uno, licencia_especial)
    else:
        segundo_mayor_q_uno = max(mes_uno, tutoria)
        minimo_q_uno = min(mes_uno, tutoria)
        
    valor_maximo_q_dos = max(mes_dos, tutoria, licencia_especial)
    if valor_maximo_q_dos == mes_dos:
        segundo_mayor_q_dos = max(tutoria, licencia_especial)
        minimo_q_dos = min(tutoria, licencia_especial)
    elif valor_maximo_q_dos == tutoria:
        segundo_mayor_q_dos = max(mes_dos, licencia_especial)
        minimo_q_dos = min(mes_dos, licencia_especial)
    else:
        segundo_mayor_q_dos = max(mes_dos, tutoria)
        minimo_q_dos = min(mes_dos, tutoria)
    
        
    ajuste_q_1 = meta_q - (meta_q*progresiones)
    ajuste_q_2 = ajuste_q_1 - (ajuste_q_1*valor_maximo)
    ajuste_q_3 = ajuste_q_2 - (ajuste_q_2*segundo_mayor)
    ajuste_q_total = round(ajuste_q_3 - (ajuste_q_3*minimo),1) ## Total Q
    
    ajuste_monto_1 = meta_monto - (meta_monto*progresiones)
    ajuste_monto_2 = ajuste_monto_1 - (ajuste_monto_1*valor_maximo)
    ajuste_monto_3 = ajuste_monto_2 - (ajuste_monto_2*segundo_mayor)
    ajuste_monto_total = int(ajuste_monto_3 - (ajuste_monto_3*minimo)) ## Total Monto
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    ajus_mes_1 = (meta_q - (meta_q*progresiones))/2
    ajus_mes_2 = ajus_mes_1 - (ajus_mes_1 * (valor_maximo_q_uno/2))
    ajus_mes_3 = ajus_mes_2 - (ajus_mes_2 * (segundo_mayor_q_uno/2))
    ajus_q_mes_uno = round((ajus_mes_3 - (ajus_mes_3 * minimo_q_uno)),1) ## ajuste Q mes 1
    
    ajus2_mes_1 = (meta_monto - (meta_monto*progresiones))/2
    ajus2_mes_2 = ajus2_mes_1 - (ajus2_mes_1 * (valor_maximo_q_uno/2))
    ajus2_mes_3 = ajus2_mes_2 - (ajus2_mes_2 * (segundo_mayor_q_uno/2))
    ajus_monto_mes_uno = int((ajus2_mes_3 - (ajus2_mes_3 * minimo_q_uno)))  ## ajuste monto mes 1
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    ajus_q_2mes_1 = (meta_q - (meta_q*progresiones))/2
    ajus_q_2mes_2 = ajus_q_2mes_1 - (ajus_q_2mes_1 * (valor_maximo_q_dos/2))
    ajus_q_2mes_3 = ajus_q_2mes_2 - (ajus_q_2mes_2 * (segundo_mayor_q_dos/2))
    ajus_q_mes_dos = round((ajus_q_2mes_3 - (ajus_q_2mes_3 * minimo_q_uno)),1) ## ajuste Q mes 2
    
    ajus2_m_mes_1 = (meta_monto - (meta_monto*progresiones))/2
    ajus2_m_mes_2 = ajus2_m_mes_1 - (ajus2_m_mes_1 * (valor_maximo_q_dos/2))
    ajus2_m_mes_3 = ajus2_m_mes_2 - (ajus2_m_mes_2 * (segundo_mayor_q_dos/2))
    ajus_monto_mes_dos = int((ajus2_m_mes_3 - (ajus2_m_mes_3 * minimo_q_dos)))  ## ajuste monto mes 2
    
        
    total_ajustes = progresiones + mes_uno + mes_dos + tutoria + licencia_especial
    if total_ajustes >= 1:
        ajus_q_mes_uno = 0
        ajus_monto_mes_uno = 0
        ajus_q_mes_dos = 0
        ajus_monto_mes_dos = 0
        ajuste_q_total = 0
        ajuste_monto_total = 0
    
    update_query = "UPDATE tec_nominaAllDataVM SET ajuste_q_mes_uno = ?, ajuste_monto_mes_uno = ?, ajuste_q_mes_dos = ?, ajuste_monto_mes_dos = ?, ajuste_total_q = ?, ajuste_total_monto = ? WHERE employeeNumber = ?"
    cursor.execute(update_query, (ajus_q_mes_uno, ajus_monto_mes_uno, ajus_q_mes_dos, ajus_monto_mes_dos, ajuste_q_total, ajuste_monto_total, legajo))    
    
    print(f'meta q: {meta_q}')
    print(f'meta monto: {meta_monto}')
    print(f'progresiones: {progresiones}')
    print(f'licencia mes uno: {mes_uno}')
    print(f'licencia mes dos: {mes_dos}')
    print(f'tutoria: {tutoria}')
    print(f'licencia_especial: {licencia_especial}')
    print('--------------------------------------')
    print(f'total ajustes: {total_ajustes}')
    print(f'total licencias----: {total_licencias}')
    print(f'ajuste q mes 1----: {ajus_q_mes_uno}')
    print(f'ajuste q mes 2----: {ajus_q_mes_dos}')
    print(f'ajuste monto mes 1----: {ajus_monto_mes_uno}')
    print(f'ajuste monto mes 2----: {ajus_monto_mes_dos}')
    print(f'ajuste total q----: {ajuste_q_total}')
    print(f'ajuste total monto----: {ajuste_monto_total}')
    
    connection.commit()    
    connection.close()





legajo = 5155
prueba(legajo)




