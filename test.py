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

def ajustes_licencias_mes_uno(legajo):
    licencia = 0
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()        
        licence_query = """
                select startDay, endDay 
                    from tec_licencesReports 
                    where employeeNumber = ?
            """
        cursor.execute(licence_query, legajo)
        licence_special = cursor.fetchall()
        for row_licencia in licence_special:
            fecha_desde = row_licencia[0]
            fecha_hasta = row_licencia[1]
            print(f'Fecha desde: {fecha_desde}')
            print(f'Fecha hasta: {fecha_hasta}')
            
            if fecha_desde.month == bimestre_actual()[0] and fecha_hasta.month == bimestre_actual()[0]:
                diferencia_dias = (fecha_hasta - fecha_desde).days + 1
                licencia += diferencia_dias * 0.01
            
        connection.close()
        print(licencia)
        return licencia
    except Exception as e:
        print(f'Error en la obtención de datos: {str(e)}')
        return licencia


legajo = 1111
print(bimestre_actual()[0])
print(dias_del_mes_bimestre()[0])
print(f'Resultado de la consulta: {ajustes_licencias_mes_uno(legajo)}')




