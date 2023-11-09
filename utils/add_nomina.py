from db.conection import DatabaseConnection

def agregar_meta_q(categoria):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query_metas = "SELECT q FROM tec_metasVM WHERE category = ?"
        cursor.execute(select_query_metas, categoria)
        meta = cursor.fetchone()
        if meta:
            update_query = "UPDATE tec_nominaAllDataVM SET metas_q = ? WHERE category = ?"
            cursor.execute(update_query, meta.q, categoria)
            connection.commit()
        cursor.close()
    except Exception as e:
        print(f'Error al agregar meta a usuarios: {str(e)}')
               
def agregar_meta_monto(categoria):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query_metas_monto = "SELECT monto FROM tec_metasVM WHERE category = ?"
        cursor.execute(select_query_metas_monto, categoria)
        meta_monto = cursor.fetchone()
        if meta_monto:
            update_query = "UPDATE tec_nominaAllDataVM SET metas_monto = ? WHERE category = ?"
            cursor.execute(update_query, meta_monto.monto, categoria)
            connection.commit()
        cursor.close()
    except Exception as e:
        print(f'Error al agregar meta a usuarios: {str(e)}')
        
def agregar_descripcion_licencias(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query_descripciones = "SELECT descriptions FROM tec_licencesReports WHERE employeeNumber = ?"
        cursor.execute(select_query_descripciones, legajo)
        descripciones = cursor.fetchall()
        descripciones_concatenadas = " - ".join(descripcion[0] for descripcion in descripciones)
        update_query = "UPDATE tec_nominaAllDataVM SET descripcion_licencias = ? WHERE employeeNumber = ?"
        cursor.execute(update_query, descripciones_concatenadas, legajo)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f'Error al agregar descripciones de licencias: {str(e)}')
        
def agregar_dias_licencias(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query_dias = "SELECT filterDays FROM tec_licencesReports WHERE employeeNumber = ?"
        cursor.execute(select_query_dias, legajo)
        dias_licencia = cursor.fetchall()
        dias_licencia_concatenadas = " - ".join(str(descripcion[0]) for descripcion in dias_licencia)
        update_query = "UPDATE tec_nominaAllDataVM SET dias_licencias = ? WHERE employeeNumber = ?"
        cursor.execute(update_query, dias_licencia_concatenadas, legajo)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f'Error al agregar descripciones de licencias: {str(e)}')

def agregar_licencias_especiales(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query_licencias_especiales = "SELECT license FROM tec_licencesSpecialReports WHERE employeeNumber = ?"
        cursor.execute(select_query_licencias_especiales, legajo)
        licencias_especiales = cursor.fetchall()
        licencias_especiales_concatenadas = " - ".join(str(licencia[0]) for licencia in licencias_especiales)
        update_query = "UPDATE tec_nominaAllDataVM SET licencias_especiales = ? WHERE employeeNumber = ?"
        cursor.execute(update_query, licencias_especiales_concatenadas, legajo)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f'Error al agregar licencias especiales: {str(e)}')
        
def agregar_dias_licencias_especiales(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query_licencias_especiales = "SELECT licenseDays FROM tec_licencesSpecialReports WHERE employeeNumber = ?"
        cursor.execute(select_query_licencias_especiales, legajo)
        licencias_especiales = cursor.fetchall()
        licencias_especiales_concatenadas = " - ".join(str(licencia[0]) for licencia in licencias_especiales)
        update_query = "UPDATE tec_nominaAllDataVM SET dias_licencias_especiales = ? WHERE employeeNumber = ?"
        cursor.execute(update_query, licencias_especiales_concatenadas, legajo)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f'Error al agregar licencias especiales: {str(e)}')
        
def agregar_progresion_si(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        update_query = "UPDATE tec_nominaAllDataVM SET tiene_progresion = 'SI' WHERE employeeNumber = ?"
        cursor.execute(update_query, legajo)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Error al agregar licencias especiales: {str(e)}')
        
def agregar_progresion_no(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        update_query = "UPDATE tec_nominaAllDataVM SET tiene_progresion = 'NO' WHERE employeeNumber = ?"
        cursor.execute(update_query, legajo)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Error al agregar licencias especiales: {str(e)}')
        
def agregar_tutor_si(employeeNumber):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        update_query = "UPDATE tec_nominaAllDataVM SET es_tutor = 'SI' WHERE employeeNumber = ?"
        cursor.execute(update_query, employeeNumber)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Error al agregar tutor: {str(e)}')
        
def agregar_tutor_no(employeeNumber):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        update_query = "UPDATE tec_nominaAllDataVM SET es_tutor = 'NO' WHERE employeeNumber = ?"
        cursor.execute(update_query, employeeNumber)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Error al agregar tutor: {str(e)}')        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        