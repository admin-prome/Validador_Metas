from flask import render_template, redirect, url_for, request

class Vistas:
    def vista_nomina(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_nominaAllDataVM"
        cursor.execute(select_query)
        nomina = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('nomina.html', nomina=nomina)
    
    def obtener_licencias(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_licencesReports"
        cursor.execute(select_query)
        licencias = cursor.fetchall()
        cursor.close()
        connection.close()
        return licencias

    def obtener_metas(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_metasVM"
        cursor.execute(select_query)
        metas = cursor.fetchall()
        cursor.close()
        connection.close()
        return metas

    def obtener_progresiones(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_progretionVM"
        cursor.execute(select_query)
        progresiones = cursor.fetchall()
        cursor.close()
        connection.close()
        return progresiones

    def obtener_users(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_usersVM"
        cursor.execute(select_query)
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users

    def obtener_usuarios_con_progresion(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_progretionOfUsers"
        cursor.execute(select_query)
        usuarios = cursor.fetchall()
        cursor.close()
        connection.close()
        return usuarios

    def obtener_tutores(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_tutoresVM"
        cursor.execute(select_query)
        tutores = cursor.fetchall()
        cursor.close()
        connection.close()
        return tutores

    def obtener_licencias_especiales(self, conexion):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT * FROM tec_licencesSpecialReports"
        cursor.execute(select_query)
        licencias = cursor.fetchall()
        cursor.close()
        connection.close()
        return licencias


    def perfil_index(self, conexion, mail):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT perfil, fullName FROM tec_usersVM WHERE mail = ?"
        cursor.execute(select_query, mail)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            perfil = result[0]
            nombre = result[1]
        else:
            perfil, nombre = None, None
        return perfil, nombre

    def obtener_observacion(self, conexion, legajo):
        connection = conexion.connect()
        cursor = connection.cursor()
        select_query = "SELECT fullName, Observacion FROM tec_nominaAllDataVM WHERE employeeNumber = ?"
        cursor.execute(select_query, (legajo,))
        observacion = cursor.fetchone()
        cursor.close()
        connection.close()
        return observacion


        
def eliminar_observacion(conexion, legajo):
    try:
        connection = conexion.connect()
        cursor = connection.cursor()
        delete_query = "UPDATE tec_nominaAllDataVM SET Observacion = '' WHERE employeeNumber = ?"
        cursor.execute(delete_query, (legajo,))
        connection.commit()
    except Exception as e:
        print(f'Error al eliminar Observacion en la base de datos: {str(e)}')
    finally:
        cursor.close()
        connection.close()

