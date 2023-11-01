from datetime import datetime
import json



def get_meta_q(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return int(meta['cantidad'])
    return ""

def get_meta_monto(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return int(meta['monto'])
    return ""

def descripcion_licencias(legajo):
    with open('data/json/licencias.json') as file_metas:
        data_licencia = json.load(file_metas)
    licencias = data_licencia['Licenses']
    descriptions = []
    for licencia in licencias:
        if licencia['employeeNumber'] == legajo:
            description = licencia['descriptions']
            if description:
                descriptions.append(description)
    if descriptions:
        return ' - '.join(descriptions)
    else:
        return ""
    
def cantidad_licencias(legajo):
    with open('data/json/licencias.json') as file_metas:
        data_licencia = json.load(file_metas)
    licencias = data_licencia['Licenses']
    days = []
    for licencia in licencias:
        if licencia['employeeNumber'] == legajo:
            filter_days = licencia.get('filterDays', 0)
            if filter_days:
                days.append(str(filter_days))
    if days:
        return ' - '.join(days)
    else:
        return ""
  
def read_licencias_especiales():
    with open('data/json/licenciasEspeciales.json') as file_licencias:
        data_licencias = json.load(file_licencias)
    result = []
    for obj in data_licencias['Licencias']:
        result.append(obj)
        legajo = obj['employeeNumber']
    return result  
    
def has_special_licence(legajo):
    licencias_data = read_licencias_especiales()
    for licencia in licencias_data:
        if licencia['employeeNumber'] == legajo:
            return licencia['license']
    return ""

def has_special_licences_days(legajo):
    licencias_data = read_licencias_especiales()
    for licencia in licencias_data:
        if licencia['employeeNumber'] == legajo:
            return int(licencia['licenseDays'])
    return ""    

def read_tutores():
    with open('data/json/tutores.json') as file_tutores:
        data_tutores = json.load(file_tutores)
    result = []
    for obj in data_tutores['Tutores']:
        result.append(obj)
        legajo = obj['legajo']
    return result

def is_tutor(legajo):
    tutores_data = read_tutores()
    tutores_legajos = [tutor['legajo'] for tutor in tutores_data]
    if legajo in tutores_legajos:
        return "SI"
    else:
        return "No"

def read_progresiones():
    with open('data/json/progresionOfUsers.json') as file_progression:
        data_progression = json.load(file_progression)
    result = []
    for obj in data_progression['Progresion_Users']:
        result.append(obj)
        legajo = obj['legajo']
    return result
      
def has_progresiones(legajo):
    progresiones_data = read_progresiones() 
    legajos_con_progresiones = [progresion['legajo'] for progresion in progresiones_data]
    if legajo in legajos_con_progresiones:
        return "SI"
    else:
        return "No"
    
def bimestre_actual():
    mes_actual = datetime.now().month
    bimestre = (mes_actual - 1) // 2 + 1
    mes_inicial = (bimestre - 1) * 2 + 1
    mes_final = bimestre * 2 + 1
    # return list(range(mes_inicial, mes_final))
    return [9,10]

def dias_del_mes_bimestre():
    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]    
    meses_bimestre = bimestre_actual()
    dias_bimestre = [dias_por_mes[mes] for mes in meses_bimestre]    
    # return dias_bimestre
    return [30,31]

def licencia_mes_uno(legajo, descripcion_lic):
    with open('data/json/licencias.json', 'r') as json_file:
        data = json.load(json_file)
    licencias = data.get('Licenses', []) 
    bim = bimestre_actual()
    dias_bim = dias_del_mes_bimestre()
    dias_licencia = 0
    for licencia in licencias:
        if licencia['employeeNumber'] == legajo and licencia['descriptions'] == descripcion_lic:
            fecha_desde = datetime.strptime(licencia['startDay'], "%d-%m-%Y")
            fecha_hasta = datetime.strptime(licencia['endDay'], "%d-%m-%Y")

            if fecha_desde.month == bim[0] and fecha_hasta.month == bim[0]:
                dias_licencia += (fecha_hasta.day - fecha_desde.day) + 1
            if fecha_desde.month == bim[0] and fecha_hasta.month != bim[0]:
                dias_licencia += (dias_bim[0] - fecha_desde.day) + 1
            if fecha_desde.month != bim[0] and fecha_hasta.month == bim[0]:
                dias_licencia += ((dias_bim[0] + fecha_hasta.day) - dias_bim[0])

    return dias_licencia

def licencia_mes_dos(legajo, descripcion_lic):
    with open('data/json/licencias.json', 'r') as json_file:
        data = json.load(json_file)
    licencias = data.get('Licenses', [])
    bim = bimestre_actual()
    dias_bim = dias_del_mes_bimestre()
    dias_licencia = 0
    for licencia in licencias:
        if licencia['employeeNumber'] == int(legajo) and licencia['descriptions'] == str(descripcion_lic):
            fecha_desde = datetime.strptime(licencia['startDay'], "%d-%m-%Y")
            fecha_hasta = datetime.strptime(licencia['endDay'], "%d-%m-%Y")
            if fecha_desde.month == bim[1] and fecha_hasta.month == bim[1]:
                dias_licencia += (fecha_hasta.day - fecha_desde.day) + 1
            if fecha_desde.month == bim[1] and fecha_hasta.month != bim[1]:
                dias_licencia += (dias_bim[1] - fecha_desde.day) + 1
            if fecha_desde.month != bim[1] and fecha_hasta.month == bim[1]:
                dias_licencia += ((dias_bim[1] + fecha_hasta.day ) - dias_bim[1])
    return dias_licencia

def ajuste_licencias_qm1(legajo):
    with open('data/json/licencias.json', 'r') as json_file:
        data = json.load(json_file)
    licencias = data.get('Licenses', [])
    ajuste_total = 0
    user = next((u for u in licencias if u['employeeNumber'] == legajo), None)
    if user:
        Descripcion_Licencias = user['descriptions']
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
    with open('data/json/licencias.json', 'r') as json_file:
        data = json.load(json_file)
    licencias = data.get('Licenses', [])
    ajuste_total = 0
    user = next((u for u in licencias if u['employeeNumber'] == legajo), None)
    if user:
        Descripcion_Licencias = user['descriptions']
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
    with open('data/json/licencias.json', 'r') as json_file:
        data = json.load(json_file)
    licencias = data.get('Licenses', [])
    ajuste_total = 0
    user = next((u for u in licencias if u['employeeNumber'] == legajo), None)
    if user:
        Descripcion_Licencias = user['descriptions']
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
    with open('data/json/licencias.json', 'r') as json_file:
        data = json.load(json_file)
    licencias = data.get('Licenses', [])
    ajuste_total = 0
    user = next((u for u in licencias if u['employeeNumber'] == legajo), None)
    if user:
        Descripcion_Licencias = user['descriptions']
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

def ajuste_meta_q_mes_uno(categoria, legajo):
    ajuste = 0
    def meta_real_q_qm1(categoria):
        with open('data/json/metas.json', 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_q = meta['cantidad']                
                return int(meta_q)
        return 0
    
    def tutores_ec_qm1(legajo):
        with open('data/json/tutores.json', 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                return 0.2                    
        return 0
    
    def progresion_ec_qm1(categoria, legajo):
        with open('data/json/progresiones.json', 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open('data/json/progresionOfUsers.json', 'r') as file_progresionOfUsers:
            data_progresionOfUsers = json.load(file_progresionOfUsers)
            progresionOfUsers = data_progresionOfUsers['Progresion_Users']        
            for user in progresionOfUsers:
                if user['legajo'] == legajo:
                    mes_progresion = user['mes_progresion']
                    for progresion in progresiones:
                        if progresion['categoria'] == categoria:
                            ajuste = progresion[mes_progresion]
                            return ajuste
        return 0  
    
    def ajuste_licencia_especial_qm1(legajo):
        with open('data/json/licenciasEspeciales.json', 'r') as file_licencia:
            data_licencia = json.load(file_licencia)
            licencia = data_licencia['Licencias']
        for user in licencia:
            if user['employeeNumber'] == legajo and 'adjustment' in user:
                return float(user['adjustment'])        
        return 0.0
    
    meta_real = meta_real_q_qm1(categoria)
    ajuste_de_licencias = ajuste_licencias_qm1(legajo)
    ajuste_de_licencia_especial = ajuste_licencia_especial_qm1(legajo)
    ajuste_tutores = tutores_ec_qm1(legajo)
    ajuste_progresion = progresion_ec_qm1(categoria, legajo)
    ajuste_total = ajuste_tutores + ajuste_progresion + ajuste_de_licencias + ajuste_de_licencia_especial
    valor_maximo = max(ajuste_de_licencias, ajuste_de_licencia_especial, ajuste_tutores)
    if valor_maximo == ajuste_de_licencias:
        segundo_mayor = max(ajuste_de_licencia_especial, ajuste_tutores)
        menor = min(ajuste_de_licencia_especial, ajuste_tutores)
    elif valor_maximo == ajuste_de_licencia_especial:
        segundo_mayor = max(ajuste_de_licencias, ajuste_tutores)
        menor = min(ajuste_de_licencias, ajuste_tutores)
    else:
        segundo_mayor = max(ajuste_de_licencias, ajuste_de_licencia_especial)
        menor = min(ajuste_de_licencias, ajuste_de_licencia_especial)
    ajuste_uno = meta_real - (meta_real*ajuste_progresion)
    ajuste_dos = ajuste_uno - (ajuste_uno * valor_maximo)
    ajuste_tres = ajuste_dos - (ajuste_dos*segundo_mayor)
    ajuste += ajuste_tres - (ajuste_tres * menor)
    if ajuste_total >= 1:
        ajuste = 0  
    return float(round(ajuste, 2))

def ajuste_meta_q_mes_dos(categoria, legajo):
    ajuste = 0
    def meta_real_q_qm1(categoria):
        with open('data/json/metas.json', 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_q = meta['cantidad']                
                return int(meta_q)
        return 0
    
    def tutores_ec_qm1(legajo):
        with open('data/json/tutores.json', 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                return 0.2                    
        return 0
    
    def progresion_ec_qm1(categoria, legajo):
        with open('data/json/progresiones.json', 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open('data/json/progresionOfUsers.json', 'r') as file_progresionOfUsers:
            data_progresionOfUsers = json.load(file_progresionOfUsers)
            progresionOfUsers = data_progresionOfUsers['Progresion_Users']        
            for user in progresionOfUsers:
                if user['legajo'] == legajo:
                    mes_progresion = user['mes_progresion']
                    for progresion in progresiones:
                        if progresion['categoria'] == categoria:
                            ajuste = progresion[mes_progresion]
                            return ajuste
        return 0
    
    def ajuste_licencia_especial_qm1(legajo):
        with open('data/json/licenciasEspeciales.json', 'r') as file_licencia:
            data_licencia = json.load(file_licencia)
            licencia = data_licencia['Licencias']
        for user in licencia:
            if user['employeeNumber'] == legajo and 'adjustment' in user:
                return float(user['adjustment'])        
        return 0.0
    
    meta_real = meta_real_q_qm1(categoria)
    ajuste_de_licencias = ajuste_licencias_qm2(legajo)
    ajuste_de_licencia_especial = ajuste_licencia_especial_qm1(legajo)
    ajuste_tutores = tutores_ec_qm1(legajo)
    ajuste_progresion = progresion_ec_qm1(categoria, legajo)
    ajuste_total = ajuste_tutores + ajuste_progresion + ajuste_de_licencias + ajuste_de_licencia_especial
    valor_maximo = max(ajuste_de_licencias, ajuste_de_licencia_especial, ajuste_tutores)
    if valor_maximo == ajuste_de_licencias:
        segundo_mayor = max(ajuste_de_licencia_especial, ajuste_tutores)
        menor = min(ajuste_de_licencia_especial, ajuste_tutores)
    elif valor_maximo == ajuste_de_licencia_especial:
        segundo_mayor = max(ajuste_de_licencias, ajuste_tutores)
        menor = min(ajuste_de_licencias, ajuste_tutores)
    else:
        segundo_mayor = max(ajuste_de_licencias, ajuste_de_licencia_especial)
        menor = min(ajuste_de_licencias, ajuste_de_licencia_especial)
    ajuste_uno = meta_real - (meta_real*ajuste_progresion)
    ajuste_dos = ajuste_uno - (ajuste_uno * valor_maximo)
    ajuste_tres = ajuste_dos - (ajuste_dos*segundo_mayor)
    ajuste += ajuste_tres - (ajuste_tres * menor)
    if ajuste_total >= 1:
        ajuste = 0
    return float(round(ajuste, 2))

def ajuste_meta_monto_m1(categoria, legajo):
    ajuste = 0
    def meta_real_monto(categoria):
        with open('data/json/metas.json', 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_monto = meta['monto']
                return meta_monto
        return 0

    def tutores_ec(legajo):
        with open('data/json/tutores.json', 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                    return 0.2                
        return 0

    def progresion_ec(categoria, legajo):  
        with open('data/json/progresiones.json', 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open('data/json/progresionOfUsers.json', 'r') as file_progresionOfUsers:
            data_progresionOfUsers = json.load(file_progresionOfUsers)
            progresionOfUsers = data_progresionOfUsers['Progresion_Users']        
            for user in progresionOfUsers:
                if user['legajo'] == legajo:
                    mes_progresion = user['mes_progresion']
                    for progresion in progresiones:
                        if progresion['categoria'] == categoria:
                            ajuste = progresion[mes_progresion]
                            return ajuste
        return 0
    
    def ajuste_licencia_especial(legajo):
        with open('data/json/licenciasEspeciales.json', 'r') as file_licencia:
            data_licencia = json.load(file_licencia)
            licencia = data_licencia['Licencias']
        for user in licencia:
            if user['employeeNumber'] == legajo and 'adjustment' in user:
                return float(user['adjustment'])        
        return 0.0

    meta_real = meta_real_monto(categoria)
    ajuste_de_licencias = ajuste_licencias_monto_uno(legajo)
    ajuste_de_licencia_especial = ajuste_licencia_especial(legajo)
    ajuste_tutores = tutores_ec(legajo)
    ajuste_progresion = progresion_ec(categoria, legajo)
    ajuste_total = ajuste_tutores + ajuste_progresion + ajuste_de_licencias + ajuste_de_licencia_especial
    valor_maximo = max(ajuste_de_licencias, ajuste_de_licencia_especial, ajuste_tutores)
    if valor_maximo == ajuste_de_licencias:
        segundo_mayor = max(ajuste_de_licencia_especial, ajuste_tutores)
        menor = min(ajuste_de_licencia_especial, ajuste_tutores)
    elif valor_maximo == ajuste_de_licencia_especial:
        segundo_mayor = max(ajuste_de_licencias, ajuste_tutores)
        menor = min(ajuste_de_licencias, ajuste_tutores)
    else:
        segundo_mayor = max(ajuste_de_licencias, ajuste_de_licencia_especial)
        menor = min(ajuste_de_licencias, ajuste_de_licencia_especial)
    ajuste_uno = meta_real - (meta_real*ajuste_progresion)
    ajuste_dos = ajuste_uno - (ajuste_uno * valor_maximo)
    ajuste_tres = ajuste_dos - (ajuste_dos*segundo_mayor)
    ajuste += ajuste_tres - (ajuste_tres * menor)
    if ajuste_total >= 1:
        ajuste = 0  
    return int(ajuste)

def ajuste_meta_monto_m2(categoria, legajo):
    ajuste = 0
    def meta_real_monto(categoria):
        with open('data/json/metas.json', 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_monto = meta['monto']
                return meta_monto
        return 0

    def tutores_ec(legajo):
        with open('data/json/tutores.json', 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                    return 0.2                
        return 0

    def progresion_ec(categoria, legajo):  
        with open('data/json/progresiones.json', 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open('data/json/progresionOfUsers.json', 'r') as file_progresionOfUsers:
            data_progresionOfUsers = json.load(file_progresionOfUsers)
            progresionOfUsers = data_progresionOfUsers['Progresion_Users']        
            for user in progresionOfUsers:
                if user['legajo'] == legajo:
                    mes_progresion = user['mes_progresion']
                    for progresion in progresiones:
                        if progresion['categoria'] == categoria:
                            ajuste = progresion[mes_progresion]
                            return ajuste
        return 0
    
    def ajuste_licencia_especial(legajo):
        with open('data/json/licenciasEspeciales.json', 'r') as file_licencia:
            data_licencia = json.load(file_licencia)
            licencia = data_licencia['Licencias']
        for user in licencia:
            if user['employeeNumber'] == legajo and 'adjustment' in user:
                return float(user['adjustment'])        
        return 0.0

    meta_real = meta_real_monto(categoria)
    ajuste_de_licencias = ajuste_licencias_monto_dos(legajo)
    ajuste_de_licencia_especial = ajuste_licencia_especial(legajo)
    ajuste_tutores = tutores_ec(legajo)
    ajuste_progresion = progresion_ec(categoria, legajo)
    ajuste_total = ajuste_tutores + ajuste_progresion + ajuste_de_licencias + ajuste_de_licencia_especial
    valor_maximo = max(ajuste_de_licencias, ajuste_de_licencia_especial, ajuste_tutores)
    if valor_maximo == ajuste_de_licencias:
        segundo_mayor = max(ajuste_de_licencia_especial, ajuste_tutores)
        menor = min(ajuste_de_licencia_especial, ajuste_tutores)
    elif valor_maximo == ajuste_de_licencia_especial:
        segundo_mayor = max(ajuste_de_licencias, ajuste_tutores)
        menor = min(ajuste_de_licencias, ajuste_tutores)
    else:
        segundo_mayor = max(ajuste_de_licencias, ajuste_de_licencia_especial)
        menor = min(ajuste_de_licencias, ajuste_de_licencia_especial)
    ajuste_uno = meta_real - (meta_real*ajuste_progresion)
    ajuste_dos = ajuste_uno - (ajuste_uno * valor_maximo)
    ajuste_tres = ajuste_dos - (ajuste_dos*segundo_mayor)
    ajuste += ajuste_tres - (ajuste_tres * menor)
    if ajuste_total >= 1:
        ajuste = 0  
    return int(ajuste)

def ajuste_total_q(categoria, legajo):
    ajuste_q_mes_1 = ajuste_meta_q_mes_uno(categoria, legajo)
    ajuste_q_mes_2 = ajuste_meta_q_mes_dos(categoria, legajo)
    result = (ajuste_q_mes_1/2) + (ajuste_q_mes_2/2)    
    return float(round(result,2))

def ajuste_total_monto(categoria, legajo):
    ajuste_monto_mes_1 = ajuste_meta_monto_m1(categoria, legajo)
    ajuste_monto_mes_2 = ajuste_meta_monto_m2(categoria, legajo)
    result = (ajuste_monto_mes_1/2) + (ajuste_monto_mes_2/2)    
    return float(result)

    
legajo = 2389	
categoria = 'C-SE - EC Senior'
descripcion_licencia = '3553-Vacaciones'

print(f'get_meta_q: {get_meta_q(categoria)}')
print(f'get_meta_monto: {get_meta_monto(categoria)}')
print(f'descripcion_licencias: {descripcion_licencias(legajo)}')
print(f'cantidad_licencias: {cantidad_licencias(legajo)}')
print(f'has_special_licence: {has_special_licence(legajo)}')
print(f'has_special_licences_days: {has_special_licences_days(legajo)}')
print(f'is_tutor: {is_tutor(legajo)}')
print(f'has_progresiones: {has_progresiones(legajo)}')
print(f'bimestre_actual: {bimestre_actual()}')
print(f'dias_del_mes_bimestre: {dias_del_mes_bimestre()}')
print(f'licencia_mes_uno: {licencia_mes_uno(legajo, descripcion_licencia)}')
print(f'licencia_mes_dos: {licencia_mes_dos(legajo, descripcion_licencia)}')
print(f'ajuste_licencias_qm1: {ajuste_licencias_qm1(legajo)}')
print(f'ajuste_licencias_qm2: {ajuste_licencias_qm2(legajo)}')
print(f'ajuste_licencias_monto_uno: {ajuste_licencias_monto_uno(legajo)}')
print(f'ajuste_licencias_monto_dos: {ajuste_licencias_monto_dos(legajo)}')
print(f'ajuste_meta_q_mes_uno: {ajuste_meta_q_mes_uno(categoria, legajo)/2}')
print(f'ajuste_meta_q_mes_dos: {ajuste_meta_q_mes_dos(categoria, legajo)/2}')
print(f'ajuste_meta_monto_m1: {ajuste_meta_monto_m1(categoria, legajo)/2}')
print(f'ajuste_meta_monto_m2: {ajuste_meta_monto_m2(categoria, legajo)/2}')
print(f'ajuste_total_q: {ajuste_total_q(categoria, legajo)}')
print(f'ajuste_total_monto: {ajuste_total_monto(categoria, legajo)}')


