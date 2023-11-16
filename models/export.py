from flask import send_file
from export.export_data import *

class ExportExcel():
    def export_excel(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        query = """select 
                        employeeNumber, 
                        fullName, 
                        branch, 
                        category, 
                        metas_q, 
                        metas_monto, 
                        descripcion_licencias, 
                        dias_licencias, 
                        licencias_especiales, 
                        dias_licencias_especiales, 
                        es_tutor, 
                        tiene_progresion, 
                        ajuste_q_mes_uno, 
                        ajuste_monto_mes_uno, 
                        ajuste_q_mes_dos, 
                        ajuste_monto_mes_dos, 
                        ajuste_total_q, 
                        ajuste_total_monto, 
                        Observacion 
                    from tec_nominaAllDataVM
                    """
        cursor.execute(query)
        nomina = cursor.fetchall()
        connection.close()    
        excel_file = export_to_excel(nomina)
        print('Listo')
        return send_file(excel_file, as_attachment=True)
    
    def export_excel_azure(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        query = """
                select 
                    employeeNumber, 
                    fullName, 
                    branch, 
                    category, 
                    metas_q, 
                    metas_monto, 
                    descripcion_licencias, 
                    dias_licencias, 
                    licencias_especiales, 
                    dias_licencias_especiales, 
                    es_tutor, 
                    tiene_progresion, 
                    ajuste_q_mes_uno, 
                    ajuste_monto_mes_uno, 
                    ajuste_q_mes_dos, 
                    ajuste_monto_mes_dos, 
                    ajuste_total_q, 
                    ajuste_total_monto, 
                    Observacion 
                from tec_nominaAllDataVM
                """
        cursor.execute(query)
        nomina = cursor.fetchall()
        connection.close()    
        excel_file = export_to_excel(nomina)
        return send_file(excel_file, 
                        as_attachment=True)
    
    
    
    