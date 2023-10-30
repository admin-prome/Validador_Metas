import json
import os
from datetime import datetime
from db.conection import DatabaseConnection 
from utils.licencias import *


def ajuste_meta_q_mes_uno(categoria, legajo):
    ajuste = 0
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_metas = os.path.join(current_dir, 'data', 'json', 'metas.json')
    json_path_tutores = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    json_path_progresiones = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    json_path_progresionOfUsers = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    json_path_licencias_especiales = os.path.join(current_dir, 'data', 'json', 'licenciasEspeciales.json')    

    def meta_real_q_qm1(categoria):
        with open(json_path_metas, 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_q = meta['cantidad']                
                return int(meta_q)
        return 0
    
    def tutores_ec_qm1(legajo):
        with open(json_path_tutores, 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                return 0.2                    
        return 0
    
    def progresion_ec_qm1(categoria, legajo):
        with open(json_path_progresiones, 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open(json_path_progresionOfUsers, 'r') as file_progresionOfUsers:
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
    
    def ajuste_licencia_especial_qm1(legajo):
        with open(json_path_licencias_especiales, 'r') as file_licencia:
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
    if ajuste_total >= 1:
        ajuste = 0
    ajuste_uno = meta_real - (meta_real*ajuste_de_licencias)
    ajuste_dos = meta_real - (ajuste_uno*ajuste_de_licencia_especial)
    print(f'meta: {meta_real}')
    print(f'licencia: {ajuste_de_licencias}')
    print(f'licencia especial {ajuste_de_licencia_especial}')
    print(f'tutores {ajuste_tutores}')
    print(f'progresion {ajuste_progresion}')
    print(f'ajuste de licencias: {ajuste_uno}')
    print(f'ajuste de licencia especial: {ajuste_dos}')
    print(f'ajuste total: {ajuste_total}')
    if ajuste_tutores > ajuste_progresion:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_tutores)
        ajuste = ajuste_meta_final - (ajuste_meta_final*ajuste_progresion)
    else:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_progresion)
        ajuste = ajuste_meta_final - (ajuste_meta_final*ajuste_tutores)           
    print(f'ajuste : {ajuste}')      
    return float(ajuste)

def ajuste_meta_q_mes_dos(categoria, legajo):
    ajuste_mes_dos = 0
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_metas = os.path.join(current_dir, 'data', 'json', 'metas.json')
    json_path_tutores = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    json_path_progresiones = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    json_path_progresionOfUsers = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    json_path_licencias_especiales = os.path.join(current_dir, 'data', 'json', 'licenciasEspeciales.json')    

    def meta_real_q_qm1(categoria):
        with open(json_path_metas, 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_q = meta['cantidad']                
                return int(meta_q)
        return 0
    
    def tutores_ec_qm1(legajo):
        with open(json_path_tutores, 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                return 0.2                    
        return 0
    
    def progresion_ec_qm1(categoria, legajo):
        with open(json_path_progresiones, 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open(json_path_progresionOfUsers, 'r') as file_progresionOfUsers:
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
    
    def ajuste_licencia_especial_qm1(legajo):
        with open(json_path_licencias_especiales, 'r') as file_licencia:
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
    if ajuste_total >= 1:
        ajuste_mes_dos = 0
    ajuste_uno = meta_real - (meta_real*ajuste_de_licencias)
    ajuste_dos = ajuste_uno - (ajuste_uno*ajuste_de_licencia_especial)
    print(f'meta: {meta_real}')
    print(f'licencia: {ajuste_de_licencias}')
    print(f'licencia especial {ajuste_de_licencia_especial}')
    print(f'tutores {ajuste_tutores}')
    print(f'progresion {ajuste_progresion}')
    print(f'ajuste de licencias: {ajuste_uno}')
    print(f'ajuste de licencia especial: {ajuste_dos}')
    print(f'ajuste total: {ajuste_total}')
    if ajuste_tutores > ajuste_progresion:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_tutores)
        ajuste_mes_dos = ajuste_meta_final - (ajuste_meta_final*ajuste_progresion)
    else:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_progresion)
        ajuste_mes_dos = ajuste_meta_final - (ajuste_meta_final*ajuste_tutores)
    
    print(f'ajuste : {ajuste_mes_dos}')
    return float(ajuste_mes_dos)


def ajuste_meta_monto_m1(categoria, legajo):
    result = 0    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_metas = os.path.join(current_dir, 'data', 'json', 'metas.json')
    json_path_tutores = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    json_path_progresiones = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    json_path_progresionOfUsers = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    json_path_licencias_especiales = os.path.join(current_dir, 'data', 'json', 'licenciasEspeciales.json')

    def meta_real_monto(categoria):
        with open(json_path_metas, 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_monto = meta['monto']
                return meta_monto
        return 0

    def tutores_ec(legajo):
        with open(json_path_tutores, 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                    return 0.2                
        return 0

    def progresion_ec(categoria, legajo):  
        with open(json_path_progresiones, 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open(json_path_progresionOfUsers, 'r') as file_progresionOfUsers:
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
    
    def ajuste_licencias_mm1(legajo):
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
    
    def ajuste_licencia_especial(legajo):
        with open(json_path_licencias_especiales, 'r') as file_licencia:
            data_licencia = json.load(file_licencia)
            licencia = data_licencia['Licencias']
        for user in licencia:
            if user['employeeNumber'] == legajo and 'adjustment' in user:
                return float(user['adjustment'])        
        return 0.0

    meta_real = meta_real_monto(categoria)
    ajuste_licencia = ajuste_licencias_mm1(legajo)
    ajuste_licencia_especial = ajuste_licencia_especial(legajo)
    ajuste_tutores = tutores_ec(legajo)
    ajuste_progresion = progresion_ec(categoria, legajo)
    ajuste_total = ajuste_licencia +  ajuste_licencia_especial + ajuste_tutores + ajuste_progresion
    if ajuste_total >= 1:
        result = 0        
    ajuste_uno = meta_real - (meta_real*ajuste_licencia)
    ajuste_dos = ajuste_uno - (ajuste_uno*ajuste_licencia_especial)
    if ajuste_tutores > ajuste_progresion:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_tutores)
        result = ajuste_meta_final - (ajuste_meta_final*ajuste_progresion)
    else:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_progresion)
        result = ajuste_meta_final - (ajuste_meta_final*ajuste_tutores)
    print(f'meta: {meta_real}')    
    print(f'licencia: {ajuste_licencia}')    
    print(f'licencia especial: {ajuste_licencia_especial}')    
    print(f'tutores: {ajuste_tutores}')    
    print(f'progresion: {ajuste_progresion}')    
    print(f'ajustes: {ajuste_total}')    
    print(f'ajustes licencia: {ajuste_uno}')    
    print(f'ajustes licencia total: {ajuste_dos}')    
    print(f'total: {result}')    
    
    
    return int(result)

def ajuste_meta_monto_m2(categoria, legajo):
    result = 0    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_metas = os.path.join(current_dir, 'data', 'json', 'metas.json')
    json_path_tutores = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    json_path_progresiones = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    json_path_progresionOfUsers = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    json_path_licencias_especiales = os.path.join(current_dir, 'data', 'json', 'licenciasEspeciales.json')

    def meta_real_monto(categoria):
        with open(json_path_metas, 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_monto = meta['monto']
                return meta_monto
        return 0

    def tutores_ec(legajo):
        with open(json_path_tutores, 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                    return 0.2                
        return 0

    def progresion_ec(categoria, legajo):  
        with open(json_path_progresiones, 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open(json_path_progresionOfUsers, 'r') as file_progresionOfUsers:
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
        with open(json_path_licencias_especiales, 'r') as file_licencia:
            data_licencia = json.load(file_licencia)
            licencia = data_licencia['Licencias']
        for user in licencia:
            if user['employeeNumber'] == legajo and 'adjustment' in user:
                return float(user['adjustment'])        
        return 0.0

    meta_real = meta_real_monto(categoria)
    ajuste_licencia = ajuste_licencias_monto_dos(legajo)
    ajuste_licencia_especial = ajuste_licencia_especial(legajo)
    ajuste_tutores = tutores_ec(legajo)
    ajuste_progresion = progresion_ec(categoria, legajo)
    ajuste_total = ajuste_licencia + ajuste_licencia_especial + ajuste_tutores + ajuste_progresion
    if ajuste_total >= 1:
        result = 0        
    ajuste_uno = meta_real - (meta_real*ajuste_licencia)
    ajuste_dos = ajuste_uno - (ajuste_uno*ajuste_licencia_especial)
    if ajuste_tutores > ajuste_progresion:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_tutores)
        result = ajuste_meta_final - (ajuste_meta_final*ajuste_progresion)
    else:
        ajuste_meta_final = ajuste_dos-(ajuste_dos*ajuste_progresion)
        result = ajuste_meta_final - (ajuste_meta_final*ajuste_tutores)
        
    print(f'meta: {meta_real}')    
    print(f'licencia: {ajuste_licencia}')    
    print(f'licencia especial: {ajuste_licencia_especial}')    
    print(f'tutores: {ajuste_tutores}')    
    print(f'progresion: {ajuste_progresion}')    
    print(f'ajustes: {ajuste_total}')    
    print(f'ajustes licencia: {ajuste_uno}')    
    print(f'ajustes licencia total: {ajuste_dos}')    
    print(f'total: {result}')    
    return int(result)


legajo = 2389
# ajuste_total_q('C-SE - EC Senior', legajo)
print(f'>> ajuste_meta_q_mes_uno: {ajuste_meta_monto_m1('C-SE - EC Senior', legajo)}')
print('-----------------------------------------------------------------------------------------------------') 
print(f'>> ajuste_meta_q_mes_dos: {ajuste_meta_monto_m2('C-SE - EC Senior', legajo)}')
# print(f'>>>> ajuste total Q: {ajuste_total_q('C-SE - EC Senior', legajo)}')
# print(f'>>>> ajuste total Monto: {ajuste_total_monto('C-SE - EC Senior', legajo)}')

