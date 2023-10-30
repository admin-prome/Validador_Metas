import json


def read_tutores():
    with open('data/json/tutores.json') as file_tutores:
        data_tutores = json.load(file_tutores)
    result = []
    for obj in data_tutores['Tutores']:
        result.append(obj)
        legajo = obj['legajo']
    return result

def read_licencias_especiales():
    with open('data/json/licenciasEspeciales.json') as file_licencias:
        data_licencias = json.load(file_licencias)
    result = []
    for obj in data_licencias['Licencias']:
        result.append(obj)
        legajo = obj['employeeNumber']
    return result

def read_progresiones():
    with open('data/json/progresionOfUsers.json') as file_progression:
        data_progression = json.load(file_progression)
    result = []
    for obj in data_progression['Progresion_Users']:
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
      
def has_progresiones(legajo):
    progresiones_data = read_progresiones() 
    legajos_con_progresiones = [progresion['legajo'] for progresion in progresiones_data]
    if legajo in legajos_con_progresiones:
        return "SI"
    else:
        return "No"