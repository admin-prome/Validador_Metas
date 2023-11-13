from db.conection import DatabaseConnection


def actualizar_datos():
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        query_metas = """
                UPDATE tec_nominaAllDataVM
                SET 
                    metas_q = metas.q,
                    metas_monto = metas.monto
                FROM tec_nominaAllDataVM as nomina
                JOIN tec_metasVM as metas ON nomina.category = metas.category;
            """
        cursor.execute(query_metas)
        query_licenses = """ 
                UPDATE nomina
                SET 
                    descripcion_licencias = licencias.descriptions,
                    dias_licencias = licencias.filterDays
                FROM tec_nominaAllDataVM AS nomina
                JOIN (
                    SELECT 
                        employeeNumber,
                        STRING_AGG(CONVERT(VARCHAR(MAX), descriptions), ' - ') AS descriptions,
                        STRING_AGG(CONVERT(VARCHAR(MAX), filterDays), ' - ') AS filterDays
                    FROM tec_licencesReports
                    GROUP BY employeeNumber
                    ) AS licencias ON nomina.employeeNumber = licencias.employeeNumber;
            """
        cursor.execute(query_licenses)
        query_especiales = """
                UPDATE tec_nominaAllDataVM
                SET 
                    licencias_especiales = licenciasE.license,
                    dias_licencias_especiales = licenciasE.licenseDays
                FROM tec_nominaAllDataVM as nomina
                JOIN tec_licencesSpecialReports as licenciasE ON nomina.employeeNumber = licenciasE.employeeNumber;
            """
        cursor.execute(query_especiales)
        query_tutor_si = """
                UPDATE tec_nominaAllDataVM
                    SET 
                        es_tutor = 'SI'
                    FROM tec_nominaAllDataVM as nomina
                    JOIN tec_tutoresVM as tutores ON nomina.employeeNumber = tutores.employeeNumber;
            """
        cursor.execute(query_tutor_si)
        query_tutor_no = """
                UPDATE tec_nominaAllDataVM
                    SET es_tutor = 'NO'
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM tec_tutoresVM as tutores
                        WHERE tec_nominaAllDataVM.employeeNumber = tutores.employeeNumber);
            """
        cursor.execute(query_tutor_no)
        query_progress_si = """
                UPDATE tec_nominaAllDataVM
                    SET 
                        tiene_progresion = 'SI'
                    FROM tec_nominaAllDataVM as nomina
                    JOIN tec_progretionOfUsers as progressU ON nomina.employeeNumber = progressU.employeeNumber;                
            """
        cursor.execute(query_progress_si)
        query_progress_no = """
                UPDATE tec_nominaAllDataVM
                    SET tiene_progresion = 'NO'
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM tec_progretionOfUsers as progressU
                        WHERE tec_nominaAllDataVM.employeeNumber = progressU.employeeNumber);
            """
        cursor.execute(query_progress_no)
        query_ajus = """
                UPDATE tec_nominaAllDataVM
                    SET 
                        ajuste_q_mes_uno = metas_q/2,
                        ajuste_monto_mes_uno = metas_monto/2,
                        ajuste_q_mes_dos = metas_q/2,
                        ajuste_monto_mes_dos = metas_monto/2,
                        ajuste_total_q = metas_q,
                        ajuste_total_monto = metas_monto
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM tec_licencesReports
                        WHERE tec_nominaAllDataVM.employeeNumber = tec_licencesReports.employeeNumber
                    ) AND NOT EXISTS (
                        SELECT 1
                        FROM tec_licencesSpecialReports
                        WHERE tec_nominaAllDataVM.employeeNumber = tec_licencesSpecialReports.employeeNumber
                    ) AND NOT EXISTS (
                        SELECT 1
                        FROM tec_progretionOfUsers
                        WHERE tec_nominaAllDataVM.employeeNumber = tec_progretionOfUsers.employeeNumber
                    ) AND NOT EXISTS (
                        SELECT 1
                        FROM tec_tutoresVM
                        WHERE tec_nominaAllDataVM.employeeNumber = tec_tutoresVM.employeeNumber
                    );
            """
        cursor.execute(query_ajus)        
        connection.commit()
        cursor.close()
        print('Actualización exitosa')
    except Exception as e:
        print(f'Error en la actualización: {str(e)}')


    


        
        
        
        
        
        
        
        
        
        
        
        
        
        