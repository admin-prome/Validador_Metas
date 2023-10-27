from db.conection import DatabaseConnection 
from datetime import datetime

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

def descripcion_licencias(legajo):
    conexion = DatabaseConnection()
    connection = conexion.connect()
    cursor = connection.cursor()
    select_query = "SELECT descriptions, startDay, endDay FROM tec_licenseReports WHERE employeeNumber = ?"
    cursor.execute(select_query, (legajo,))
    result = cursor.fetchall()
    licencias_info = []
    for licencia in result:
        descripcion = str(licencia[0])
        start_date = str(licencia[1])
        end_date = str(licencia[2])
        fecha_licencia = f'{descripcion} ({start_date}) al ({end_date})'
        licencias_info.append(fecha_licencia)
    if len(licencias_info) == 1:
        return licencias_info[0]
    else:
        descripcion_final = ' - '.join(licencias_info)
        return str(descripcion_final)
    
def cantidad_licencias(legajo):
    conexion = DatabaseConnection()
    connection = conexion.connect()
    cursor = connection.cursor()
    select_query = "SELECT licenseDays FROM tec_licenseReports WHERE employeeNumber = ?"
    cursor.execute(select_query, (legajo,))
    result = cursor.fetchall()
    dias_totales = [str(licencia[0]) for licencia in result]
    if len(dias_totales) == 1:
        return dias_totales[0]    
    else:
        descripcion_final = ' - '.join(dias_totales)
        return str(descripcion_final)
    
def licencia_mes_uno(legajo, descripcion_lic):
    conexion = DatabaseConnection()
    connection = conexion.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_licenseReports WHERE employeeNumber = ?"
    cursor.execute(select_query, (legajo,))
    result = cursor.fetchall()    
    bim = bimestre_actual()
    dias_bim = dias_del_mes_bimestre()
    vacaciones = descripcion_lic
    dias_licencia = 0
    for row in result:
        descripcion = row[3]
        fecha_desde = row[4]
        fecha_hasta = row[5]
        if descripcion == vacaciones:
            if fecha_desde.month == bim[0] and fecha_hasta.month == bim[0]:
                dias_licencia += (fecha_hasta.day - fecha_desde.day) + 1
            if fecha_desde.month == bim[0] and fecha_hasta.month != bim[0]:
                dias_licencia += (dias_bim[0] - fecha_desde.day) + 1
            if fecha_desde.month != bim[0] and fecha_hasta.month == bim[0]:
                dias_licencia += ((dias_bim[0] + fecha_hasta.day ) - dias_bim[0])            
    return dias_licencia

def licencia_mes_dos(legajo, descripcion_lic):
    conexion = DatabaseConnection()
    connection = conexion.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_licenseReports WHERE employeeNumber = ?"
    cursor.execute(select_query, (legajo,))
    result = cursor.fetchall()    
    bim = bimestre_actual()
    dias_bim = dias_del_mes_bimestre()
    vacaciones = descripcion_lic
    dias_licencia = 0
    for row in result:
        descripcion = row[3]
        fecha_desde = row[4]
        fecha_hasta = row[5]
        if descripcion == vacaciones:
            if fecha_desde.month == bim[1] and fecha_hasta.month == bim[1]:
                dias_licencia += (fecha_hasta.day - fecha_desde.day) + 1
            if fecha_desde.month == bim[1] and fecha_hasta.month != bim[1]:
                dias_licencia += (dias_bim[1] - fecha_desde.day) + 1
            if fecha_desde.month != bim[1] and fecha_hasta.month == bim[1]:
                dias_licencia += ((dias_bim[1] + fecha_hasta.day ) - dias_bim[1])            
    return dias_licencia

def ajuste_licencias_qm1(legajo):
        conexion = DatabaseConnection()
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_licenseReports WHERE employeeNumber = ?"
        cursor.execute(select_query, (legajo,))
        result = cursor.fetchall()
        ajuste_total = 0
        for user in result:
            Descripcion_Licencias = user[3]
            if Descripcion_Licencias == "3553-Vacaciones":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "3553-Vacaciones")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
            if Descripcion_Licencias == "4110-Licencia por Enfermedad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4110-Licencia por Enfermedad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4070-Licencia por Matrimonio":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4070-Licencia por Matrimonio")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "2222-Licencias por Violencia de genero":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "2222-Licencias por Violencia de genero")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "3333-Licencias por Perdida Gestacional":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "3333-Licencias por Perdida Gestacional")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4104-Licencia por Accidente":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4104-Licencia por Accidente")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                   
            if Descripcion_Licencias == "11-Licencia Fertilidad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "11-Licencia Fertilidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4132-Licencia por Maternidad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4132-Licencia por Maternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4118-Beneficio Paternidad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4118-Beneficio Paternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4133-Período de Excedencia":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4133-Período de Excedencia")
                if Cant_Dias_Licencia > 0 and Cant_Dias_Licencia <= 1:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 1:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
        return ajuste_total

def ajuste_licencias_qm2(legajo):
        conexion = DatabaseConnection()
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_licenseReports WHERE employeeNumber = ?"
        cursor.execute(select_query, (legajo,))
        result = cursor.fetchall()
        ajuste_total = 0
        for user in result:
            Descripcion_Licencias = user[3]
            if Descripcion_Licencias == "3553-Vacaciones":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "3553-Vacaciones")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
            if Descripcion_Licencias == "4110-Licencia por Enfermedad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4110-Licencia por Enfermedad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4070-Licencia por Matrimonio":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4070-Licencia por Matrimonio")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "2222-Licencias por Violencia de genero":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "2222-Licencias por Violencia de genero")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "3333-Licencias por Perdida Gestacional":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "3333-Licencias por Perdida Gestacional")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4104-Licencia por Accidente":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4104-Licencia por Accidente")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                   
            if Descripcion_Licencias == "11-Licencia Fertilidad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "11-Licencia Fertilidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4132-Licencia por Maternidad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4132-Licencia por Maternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4118-Beneficio Paternidad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4118-Beneficio Paternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4133-Período de Excedencia":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4133-Período de Excedencia")
                if Cant_Dias_Licencia > 0 and Cant_Dias_Licencia <= 1:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 1:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
        return ajuste_total

def ajuste_licencias_monto_uno(legajo):
        conexion = DatabaseConnection()
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_licenseReports WHERE employeeNumber = ?"
        cursor.execute(select_query, (legajo,))
        result = cursor.fetchall()
        ajuste_total = 0
        for user in result:
            Descripcion_Licencias = user[3]
            if Descripcion_Licencias == "3553-Vacaciones":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "3553-Vacaciones")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
            if Descripcion_Licencias == "4110-Licencia por Enfermedad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4110-Licencia por Enfermedad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4070-Licencia por Matrimonio":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4070-Licencia por Matrimonio")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "2222-Licencias por Violencia de genero":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "2222-Licencias por Violencia de genero")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "3333-Licencias por Perdida Gestacional":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "3333-Licencias por Perdida Gestacional")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4104-Licencia por Accidente":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4104-Licencia por Accidente")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                   
            if Descripcion_Licencias == "11-Licencia Fertilidad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "11-Licencia Fertilidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4132-Licencia por Maternidad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4132-Licencia por Maternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4118-Beneficio Paternidad":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4118-Beneficio Paternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4133-Período de Excedencia":
                Cant_Dias_Licencia = licencia_mes_uno(legajo, "4133-Período de Excedencia")
                if Cant_Dias_Licencia > 0 and Cant_Dias_Licencia <= 1:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 1:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
        return ajuste_total

def ajuste_licencias_monto_dos(legajo):
        conexion = DatabaseConnection()
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_licenseReports WHERE employeeNumber = ?"
        cursor.execute(select_query, (legajo,))
        result = cursor.fetchall()
        ajuste_total = 0
        for user in result:
            Descripcion_Licencias = user[3]
            if Descripcion_Licencias == "3553-Vacaciones":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "3553-Vacaciones")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
            if Descripcion_Licencias == "4110-Licencia por Enfermedad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4110-Licencia por Enfermedad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4070-Licencia por Matrimonio":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4070-Licencia por Matrimonio")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "2222-Licencias por Violencia de genero":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "2222-Licencias por Violencia de genero")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "3333-Licencias por Perdida Gestacional":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "3333-Licencias por Perdida Gestacional")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4104-Licencia por Accidente":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4104-Licencia por Accidente")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                   
            if Descripcion_Licencias == "11-Licencia Fertilidad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "11-Licencia Fertilidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4132-Licencia por Maternidad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4132-Licencia por Maternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4118-Beneficio Paternidad":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4118-Beneficio Paternidad")
                if Cant_Dias_Licencia >= 7 and Cant_Dias_Licencia <=21:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 21:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0                    
            if Descripcion_Licencias == "4133-Período de Excedencia":
                Cant_Dias_Licencia = licencia_mes_dos(legajo, "4133-Período de Excedencia")
                if Cant_Dias_Licencia > 0 and Cant_Dias_Licencia <= 1:
                    ajuste_total += 0.01 * Cant_Dias_Licencia
                elif Cant_Dias_Licencia > 1:
                    ajuste_total += 1.0
                else:
                    ajuste_total += 0
        return ajuste_total

