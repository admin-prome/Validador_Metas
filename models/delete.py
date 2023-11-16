from flask import redirect, url_for, request

class Eliminar():
    def eliminar_meta(self, conexion,  categoria):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            delete_query = "DELETE FROM tec_metasVM WHERE category = ?"
            cursor.execute(delete_query, categoria)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('metas'))
        except Exception as e:
            return f'Error al eliminar la meta: {str(e)}'
        
    def delete_observacion(self, conexion):
        legajo = request.form.get('employeeNumber')
        if legajo is not None and legajo.isnumeric():
            try:
                connection = conexion.connect()
                cursor = connection.cursor()
                delete_query = "UPDATE tec_nominaAllDataVM SET Observacion = '' WHERE employeeNumber = ?"
                cursor.execute(delete_query, (int(legajo),))
                connection.commit()
            except Exception as e:
                print(f'Error al eliminar Observacion en la base de datos: {str(e)}')
            finally:
                cursor.close()
                connection.close()
        return redirect('/nomina')
    
    def eliminar_progresion(self, conexion, categoria):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            delete_query = "DELETE FROM tec_progretionVM WHERE category = ?"
            cursor.execute(delete_query, categoria)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('progresiones'))
        except Exception as e:
            return f'Error al eliminar la progresion: {str(e)}'
        
    def eliminar_user(self, conexion, legajo):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            delete_query = "DELETE FROM tec_usersVM WHERE employeeNumber = ?"
            cursor.execute(delete_query, legajo)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('users'))   
        except Exception as e:
            return f'Error al eliminar el usuario: {str(e)}'
        
    def eliminar_usuario_con_progresiones(self, conexion, legajo):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            delete_query = "DELETE FROM tec_progretionOfUsers WHERE employeeNumber = ?"
            cursor.execute(delete_query, legajo)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('usuarios_con_progresion'))
        except Exception as e:
            return f'Error al eliminar la meta: {str(e)}'
        
    def eliminar_tutores(self, conexion, legajo):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            delete_query = "DELETE FROM tec_tutoresVM WHERE employeeNumber = ?"
            cursor.execute(delete_query, legajo)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('tutores'))
        except Exception as e:
            return f'Error al eliminar la meta: {str(e)}'    
        
    def eliminar_licencia(self, conexion, employeeNumber):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            delete_query = "DELETE FROM tec_licencesSpecialReports WHERE employeeNumber = ?"
            cursor.execute(delete_query, employeeNumber)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('licencias_especiales'))
        except Exception as e:
            return f'Error al eliminar la meta: {str(e)}'   
        
        
        
        
        
        
        
        
        
        
        
        
        