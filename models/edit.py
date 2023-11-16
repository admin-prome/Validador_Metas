from flask import render_template, redirect, url_for, request
from models.views import *

vistas = Vistas()

class Edit():
    def editar_observ(self, conexion, legajo, nueva_observacion):
        try:
            connection = conexion.connect()
            cursor = connection.cursor()
            update_query = "UPDATE tec_nominaAllDataVM SET Observacion = ? WHERE employeeNumber = ?"
            cursor.execute(update_query, (nueva_observacion, legajo))
            connection.commit()
        except Exception as e:
            print(f'Error al editar Observacion en la base de datos: {str(e)}')
        finally:
            cursor.close()
            connection.close()
        if request.method == 'POST':
            nueva_observacion = request.form.get('Observacion')
            return redirect(url_for('nomina'))
        observacion = vistas.obtener_observacion(conexion,legajo)    
        return render_template('edit/editObservacion.html', legajo=legajo, fullName=observacion[0], observacion=observacion[1])
            
            
    def editar_meta(self, conexion, categoria):
        if request.method == 'POST':
            nueva_cantidad = int(request.form.get('cantidad'))
            nuevo_monto = float(request.form.get('monto'))
            nuevo_monto_prom = float(request.form.get('monto_prom'))
            nueva_fecha = request.form.get('fecha')
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_metasVM WHERE category = ?"
            cursor.execute(select_query, categoria)
            categoria_result = cursor.fetchone()[0]
            if categoria_result > 0:
                update_query = "UPDATE tec_metasVM SET q = ?, monto = ?, monto_promedio = ?, fecha = ? WHERE category = ?"
                cursor.execute(update_query, nueva_cantidad, nuevo_monto, nuevo_monto_prom, nueva_fecha, categoria)
                connection.commit()
            else:
                connection.close()
                return "La categoría no existe y no se puede editar."
            connection.close()
            return redirect(url_for('metas'))
        connection = conexion.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tec_metasVM WHERE category = ?", categoria)
        datos_categoria = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('edit/editMetas.html', datos_categoria=datos_categoria)
    
    def editar_progresion(self, conexion, categoria):
        if request.method == 'POST':
            datos_progresion_1 = float(request.form.get('month_1'))
            datos_progresion_2 = float(request.form.get('month_2'))
            datos_progresion_3 = float(request.form.get('month_3'))
            datos_progresion_4 = float(request.form.get('month_4'))
            datos_progresion_5 = float(request.form.get('month_5'))
            datos_progresion_6 = float(request.form.get('month_6'))
            connection = conexion.connect()
            cursor = connection.cursor()
            update_query = "UPDATE tec_progretionVM SET month_1 = ?, month_2 = ?, month_3 = ?, month_4 = ?, month_5 = ?, month_6 = ? WHERE category = ?"
            cursor.execute(update_query, datos_progresion_1, datos_progresion_2, datos_progresion_3, datos_progresion_4, datos_progresion_5, datos_progresion_6, categoria)
            connection.commit()
            return redirect(url_for('progresiones'))
        connection = conexion.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tec_progretionVM WHERE category = ?", categoria)
        datos_progresion = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('edit/editProgresiones.html', datos_progresion=datos_progresion)
    
    def editar_usuario(self, conexion, legajo):
        if request.method == 'POST':
            fullName = request.form['fullName']
            mail = request.form['mail']
            passw = request.form['passw']
            perfil = request.form['perfil']
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_usersVM WHERE employeeNumber = ?"
            cursor.execute(select_query, legajo)
            employeeNumber_result = cursor.fetchone()[0]
            if employeeNumber_result > 0:
                update_query = "UPDATE tec_usersVM SET fullName = ?, mail = ?, passw = ?, perfil = ? WHERE employeeNumber = ?"
                cursor.execute(update_query, fullName, mail, passw, perfil, legajo)
                connection.commit()
            else:
                cursor.close()
                connection.close()
            return redirect(url_for('users'))
        connection = conexion.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tec_usersVM WHERE employeeNumber = ?", legajo)
        datos_usuario = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('edit/editUsers.html', datos_usuario=datos_usuario)
    
    def editar_usuario_con_progresiones(self, conexion, legajo):
        if request.method == 'POST':
            fullName = request.form.get('fullName')
            category = request.form.get('category')
            adjustment = request.form.get('adjustment')
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_progretionOfUsers WHERE employeeNumber = ?"
            cursor.execute(select_query, legajo)
            categoria_result = cursor.fetchone()[0]
            if categoria_result > 0:
                update_query = "UPDATE tec_progretionOfUsers SET fullName = ?, category = ?, adjustment = ? WHERE employeeNumber = ?"
                cursor.execute(update_query, fullName, category, adjustment, legajo)
                connection.commit()
            else:
                connection.close()
                return "La categoría no existe y no se puede editar."
            return redirect(url_for('usuarios_con_progresion'))
        connection = conexion.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tec_progretionOfUsers WHERE employeeNumber = ?", legajo)
        datos_usuarioConProgresiones = cursor.fetchone()
        cursor.close()
        connection.close()            
        return render_template('edit/editUsuariosConProgresiones.html', datos_usuarioConProgresiones=datos_usuarioConProgresiones)
    
    def editar_tutores(self, conexion, legajo):    
        if request.method == 'POST':
            fullName = request.form.get('fullName')
            category = request.form.get('category')
            startDate = request.form.get('startDate')
            endDate = request.form.get('endDate')
            adjustment = float(request.form.get('adjustment'))
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_tutoresVM WHERE employeeNumber = ?"
            cursor.execute(select_query, legajo)
            categoria_result = cursor.fetchone()[0]
            if categoria_result > 0:
                update_query = "UPDATE tec_tutoresVM SET fullName = ?, category = ?, startDate = ?, endDate = ?, adjustment = ? WHERE employeeNumber = ?"
                cursor.execute(update_query, fullName, category, startDate, endDate, adjustment, legajo)
                connection.commit()
            else:
                connection.close()
                return "La categoría no existe y no se puede editar."
            return redirect(url_for('tutores'))
        connection = conexion.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tec_tutoresVM WHERE employeeNumber = ?", legajo)
        datos_tutores = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('edit/editTutores.html', datos_tutores=datos_tutores)
       
    def editar_licencia(self, conexion, employeeNumber):
        if request.method == 'POST':
            nuevo_fullName = request.form['fullName']
            nuevo_license = request.form['license']
            nuevo_licenseStar = request.form['licenseStar']
            nuevo_licenseEnd = request.form['licenseEnd']        
            nuevo_licenseDays = request.form['licenseDays']        
            nuevo_adjustment = request.form['adjustment']
            connection = conexion.connect()
            cursor = connection.cursor()        
            update_query = "UPDATE tec_licencesSpecialReports SET fullName = ?, license = ?, licenseStar = ?, licenseEnd = ?, licenseDays = ?, adjustment = ? WHERE employeeNumber = ?"
            cursor.execute(update_query, nuevo_fullName, nuevo_license, nuevo_licenseStar, nuevo_licenseEnd, nuevo_licenseDays, nuevo_adjustment, employeeNumber)
            connection.commit()
            return redirect(url_for('licencias_especiales'))
        connection = conexion.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tec_licencesSpecialReports WHERE employeeNumber = ?", employeeNumber)
        datos_licencia = cursor.fetchone()
        cursor.close()
        connection.close()    
        return render_template('edit/editLicencias.html', datos_licencia=datos_licencia)
    
    
    
    
    
    
    
    
    
    
        