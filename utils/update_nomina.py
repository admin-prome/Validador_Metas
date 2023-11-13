from datetime import datetime
from db.conection import DatabaseConnection

def bimestre_actual():
    mes_actual = datetime.now().month
    bimestre = (mes_actual - 1) // 2 + 1
    mes_inicial = (bimestre - 1) * 2 + 1
    mes_final = bimestre * 2 + 1
    return list(range(mes_inicial, mes_final))

def dias_del_mes_bimestre():
    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]    
    meses_bimestre = bimestre_actual()
    dias_bimestre = [dias_por_mes[mes] for mes in meses_bimestre]    
    return dias_bimestre

def ajustes_metas(legajo):
    bimestre = bimestre_actual()
    dias_bimestre = dias_del_mes_bimestre()
    total_q_mes_uno = 0
    total_q_mes_dos = 0
    total_q = 0
    total_monto_mes_uno = 0
    total_monto_mes_dos = 0
    total_monto = 0
    meta_q = 0
    meta_monto = 0
    ajuste_licencias = 0.01
    ajuste_tutoria = 0
    ajuste_progresion = 0
    dias_licencias_uno = 0
    dias_licencias_dos = 0
    total_licencias = dias_licencias_uno + dias_licencias_dos
    ajuste_licencia_especial = 0
    
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    nomina_query = "SELECT * FROM tec_nominaAllDataVM WHERE employeeNumber = ?"
    cursor.execute(nomina_query, legajo)
    rows_nomina = cursor.fetchall()    
    progresion_query = "SELECT * FROM tec_progretionOfUsers WHERE employeeNumber = ?"
    cursor.execute(progresion_query, legajo)
    rows_progresiones = cursor.fetchall()    
    tutores_query = "SELECT * FROM tec_tutoresVM WHERE employeeNumber = ?"
    cursor.execute(tutores_query, legajo)
    rows_tutores = cursor.fetchall()    
    licencia_query = "SELECT * FROM tec_licencesReports WHERE employeeNumber = ?"
    cursor.execute(licencia_query, legajo)
    rows_licencia = cursor.fetchall()    
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
        ajuste_progresion += ajuste_progress
        
    for row_tutor in rows_tutores:
        ajuste = row_tutor[6]
        ajuste_tutoria += ajuste
    
    for row_licencia in rows_licencia:
        fecha_desde = row_licencia[4]
        fecha_hasta = row_licencia[5]            
        if fecha_desde.month == bimestre[0] and fecha_hasta.month == bimestre[0]:
            dias_licencias_uno += ((fecha_hasta.day - fecha_desde.day) + 1)*ajuste_licencias
        if fecha_desde.month == bimestre[0] and fecha_hasta.month != bimestre[0]:
            dias_licencias_uno += ((dias_bimestre[0] - fecha_desde.day) + 1)*ajuste_licencias
        if fecha_desde.month != bimestre[0] and fecha_hasta.month == bimestre[0]:
            dias_licencias_uno += ((dias_bimestre[0] + fecha_hasta.day) - dias_bimestre[0])*ajuste_licencias              
        if fecha_desde.month == bimestre[1] and fecha_hasta.month == bimestre[1]:
            dias_licencias_dos += ((fecha_hasta.day - fecha_desde.day) + 1)*ajuste_licencias
        if fecha_desde.month == bimestre[1] and fecha_hasta.month != bimestre[1]:
            dias_licencias_dos += ((dias_bimestre[1] - fecha_desde.day) + 1)*ajuste_licencias
        if fecha_desde.month != bimestre[1] and fecha_hasta.month == bimestre[1]:
            dias_licencias_dos += ((dias_bimestre[1] + fecha_hasta.day) - dias_bimestre[1])*ajuste_licencias
    
    for rows_licen_esp in rows_licencia_especial:
        ajuste_lic_esp = rows_licen_esp[7]
        ajuste_licencia_especial += ajuste_lic_esp
    
    total_de_ajustes_mes_uno = dias_licencias_uno + (ajuste_tutoria/2) + ajuste_progresion + ajuste_licencia_especial        
    total_de_ajustes_mes_dos = dias_licencias_dos + (ajuste_tutoria/2) + ajuste_progresion + ajuste_licencia_especial        
    total_de_ajustes = total_licencias + ajuste_tutoria + ajuste_progresion + ajuste_licencia_especial        
    
    valor_maximo_mes_uno = max(dias_licencias_uno, ajuste_tutoria, ajuste_licencia_especial)    
    valor_maximo_mes_dos = max(dias_licencias_uno, ajuste_tutoria, ajuste_licencia_especial)
    valor_maximo = max(total_licencias, ajuste_tutoria, ajuste_licencia_especial)
    
    if valor_maximo_mes_uno == dias_licencias_uno:
        segundo_mayor_mes_uno = max(ajuste_tutoria, ajuste_licencia_especial)
        menor_mes_uno = min(ajuste_tutoria, ajuste_licencia_especial)
    elif valor_maximo_mes_uno == ajuste_tutoria:
        segundo_mayor_mes_uno = max(dias_licencias_uno, ajuste_licencia_especial)
        menor_mes_uno = min(dias_licencias_uno, ajuste_licencia_especial)
    else:
        segundo_mayor_mes_uno = max(dias_licencias_uno, ajuste_tutoria)
        menor_mes_uno = min(dias_licencias_uno, ajuste_tutoria)
        
    ajuste_q_1 = (meta_q/2) - ((meta_q/2)*ajuste_progresion)
    ajuste_q_2 = ajuste_q_1 - (ajuste_q_1*valor_maximo_mes_uno)
    ajuste_q_3 = ajuste_q_2 - (ajuste_q_2*segundo_mayor_mes_uno)
    ajuste_q_4 = ajuste_q_3 - (ajuste_q_3*menor_mes_uno)
    ajuste_monto_1 = (meta_monto/2) - ((meta_monto/2)*ajuste_progresion)
    ajuste_monto_2 = ajuste_monto_1 - (ajuste_monto_1*valor_maximo_mes_uno)
    ajuste_monto_3 = ajuste_monto_2 - (ajuste_monto_2*segundo_mayor_mes_uno)
    ajuste_monto_4 = ajuste_monto_3 - (ajuste_monto_3*menor_mes_uno)
    total_q_mes_uno += round(ajuste_q_4, 2)
    total_monto_mes_uno += ajuste_monto_4
    if total_de_ajustes_mes_uno >= 1:
        total_q_mes_uno = 0
        total_monto_mes_uno = 0
        
        
    if valor_maximo_mes_dos == total_licencias:
        segundo_mayor_mes_dos = max(ajuste_tutoria, ajuste_licencia_especial)
        menor_mes_dos = min(ajuste_tutoria, ajuste_licencia_especial)
    elif valor_maximo_mes_dos == ajuste_tutoria:
        segundo_mayor_mes_dos = max(total_licencias, ajuste_licencia_especial)
        menor_mes_dos = min(total_licencias, ajuste_licencia_especial)
    else:
        segundo_mayor_mes_dos = max(total_licencias, ajuste_tutoria)
        menor_mes_dos = min(total_licencias, ajuste_tutoria)
        
    ajuste_q_m2_1 = (meta_q/2) - ((meta_q/2)*ajuste_progresion)
    ajuste_q_m2_2 = ajuste_q_m2_1 - (ajuste_q_m2_1*valor_maximo_mes_dos)
    ajuste_q_m2_3 = ajuste_q_m2_2 - (ajuste_q_m2_2*segundo_mayor_mes_dos)
    ajuste_q_m2_4 = ajuste_q_m2_3 - (ajuste_q_m2_3*menor_mes_dos)
    ajuste_monto_m2_1 = (meta_monto/2) - ((meta_monto/2)*ajuste_progresion)
    ajuste_monto_m2_2 = ajuste_monto_m2_1 - (ajuste_monto_m2_1*valor_maximo_mes_dos)
    ajuste_monto_m2_3 = ajuste_monto_m2_2 - (ajuste_monto_m2_2*segundo_mayor_mes_dos)
    ajuste_monto_m2_4 = ajuste_monto_m2_3 - (ajuste_monto_m2_3*menor_mes_dos)
    total_q_mes_dos += round(ajuste_q_m2_4, 2)
    total_monto_mes_dos += ajuste_monto_m2_4
    if total_de_ajustes_mes_dos >= 1:
        total_q_mes_dos = 0
        total_monto_mes_dos = 0
        
        
    if valor_maximo == dias_licencias_dos:
        segundo_mayor = max(ajuste_tutoria, ajuste_licencia_especial)
        menor = min(ajuste_tutoria, ajuste_licencia_especial)
    elif valor_maximo == ajuste_tutoria:
        segundo_mayor = max(dias_licencias_dos, ajuste_licencia_especial)
        menor = min(dias_licencias_dos, ajuste_licencia_especial)
    else:
        segundo_mayor = max(dias_licencias_dos, ajuste_tutoria)
        menor = min(dias_licencias_dos, ajuste_tutoria)
        
    ajuste_q_total_1 = meta_q - (meta_q*ajuste_progresion)
    ajuste_q_total_2 = ajuste_q_total_1 - (ajuste_q_total_1*valor_maximo)
    ajuste_q_total_3 = ajuste_q_total_2 - (ajuste_q_total_2*segundo_mayor)
    ajuste_q_total_4 = ajuste_q_total_3 - (ajuste_q_total_3*menor)
    ajuste1monto_2 = (meta_monto/2) - ((meta_monto/2)*ajuste_progresion)
    ajuste2monto_2 = ajuste1monto_2 - (ajuste1monto_2*valor_maximo_mes_dos)
    ajuste3monto_2 = ajuste2monto_2 - (ajuste2monto_2*segundo_mayor_mes_dos)
    ajuste4monto_2 = ajuste3monto_2 - (ajuste3monto_2*menor_mes_dos)
    total_q += round(ajuste_q_total_4, 2)
    total_monto += ajuste4monto_2
    if total_de_ajustes >= 1:
        total_q = 0
        total_monto = 0
    
    update_query = "UPDATE tec_nominaAllDataVM SET ajuste_q_mes_uno = ?, ajuste_monto_mes_uno = ?, ajuste_q_mes_dos = ?, ajuste_monto_mes_dos = ?, ajuste_total_q = ?, ajuste_total_monto = ? WHERE employeeNumber = ?"
    cursor.execute(update_query, (total_q_mes_uno, total_monto_mes_uno, total_q_mes_dos, total_monto_mes_dos, total_q, total_monto, legajo))
    connection.commit()    
    connection.close()
    