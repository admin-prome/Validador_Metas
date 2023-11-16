
from flask import render_template, redirect, url_for, request

class Agregar():
    def agregar_meta(self, conexion):
        if request.method == 'POST':
            categoria = request.form['categoria']
            cantidad = int(request.form['cantidad'])
            monto = float(request.form['monto'])
            monto_prom = float(request.form['monto_prom'])
            fecha = request.form['fecha']
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_metasVM WHERE category = ?"
            cursor.execute(select_query, categoria)
            categoria_result = cursor.fetchone()[0]
            if categoria_result > 0:
                cursor.close()
                connection.close()
            else:
                insert_query = "INSERT INTO tec_metasVM (category, q, monto, monto_promedio, fecha) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(insert_query, categoria, cantidad, monto, monto_prom, fecha)
                connection.commit()
                cursor.close()
                connection.close()
            return redirect(url_for('metas'))
        return render_template('add/addMetas.html')
    
    def agregar_progresion(self, conexion):
        if request.method == 'POST':
            categoria = request.form['categoria']
            month_1 = float(request.form['month_1'])
            month_2 = float(request.form['month_2'])
            month_3 = float(request.form['month_3'])
            month_4 = float(request.form['month_4'])
            month_5 = float(request.form['month_5'])
            month_6 = float(request.form['month_6'])
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_progretionVM WHERE category = ?"
            cursor.execute(select_query, categoria)
            categoria_result = cursor.fetchone()[0]
            if categoria_result > 0:
                cursor.close()
                connection.close()
            else:
                insert_query = "INSERT INTO tec_progretionVM (category, month_1, month_2, month_3, month_4, month_5, month_6) VALUES (?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(insert_query, categoria, month_1, month_2, month_3, month_4, month_5, month_6)
                connection.commit()
                cursor.close()
                connection.close()
            return redirect(url_for('progresiones'))
        return render_template('add/addProgresiones.html')
    
    def agregar_usuario(self, conexion):
        if request.method == 'POST':
            employeeNumber = int(request.form['employeeNumber'])
            fullName = request.form['fullName']
            mail = request.form['mail']
            passw = request.form['passw']
            perfil = request.form['perfil']
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_usersVM WHERE employeeNumber = ?"
            cursor.execute(select_query, employeeNumber)
            employeeNumber_result = cursor.fetchone()[0]
            if employeeNumber_result > 0:
                cursor.close()
                connection.close()
                error_message = 'El legajo ya existe. No se permite agregar un usuario con el mismo legajo.'
                return render_template('add/addUsers.html', error_message=error_message)
            else:
                insert_query = "INSERT INTO tec_usersVM (employeeNumber, fullName, mail, passw, perfil) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(insert_query, employeeNumber, fullName, mail, passw, perfil)
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('users'))
        return render_template('add/addUsers.html')
    
    def agregar_usuario_con_progresion(self, conexion):
        if request.method == 'POST':
            employeeNumber = int(request.form['employeeNumber'])
            fullName = request.form['fullName']
            category = request.form['category']
            adjustment = float(request.form['adjustment'])
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_progretionOfUsers WHERE employeeNumber = ?"
            cursor.execute(select_query, employeeNumber)
            categoria_result = cursor.fetchone()[0]
            if categoria_result > 0:
                cursor.close()
                connection.close()
            else:
                insert_query = "INSERT INTO tec_progretionOfUsers (employeeNumber, fullName, category, adjustment) VALUES (?, ?, ?, ?)"
                cursor.execute(insert_query, employeeNumber, fullName, category, adjustment)
                connection.commit()
                cursor.close()
                connection.close()
            return redirect(url_for('usuarios_con_progresion'))
        return render_template('add/addUsuarioConProgresion.html', error_message=None)
    
    def agregar_tutor(self, conexion):
        if request.method == 'POST':
            employeeNumber = int(request.form['employeeNumber'])       
            fullName = request.form['fullName']      
            category = request.form['category']     
            startDate = request.form['startDate']       
            endDate = request.form['endDate']      
            adjustment = float(request.form['adjustment'])
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM tec_tutoresVM WHERE employeeNumber = ?"
            cursor.execute(select_query, employeeNumber)   
            legajo = cursor.fetchone()[0]
            if legajo > 0:
                cursor.close()
                connection.close()
            else:    
                insert_query = "INSERT INTO tec_tutoresVM (employeeNumber, fullName, category, startDate, endDate, adjustment) VALUES (?, ?, ?, ?, ?, ?)"
                cursor.execute(insert_query, employeeNumber, fullName, category, startDate, endDate, adjustment)
                connection.commit()
                cursor.close()
                connection.close()
            return redirect(url_for('tutores'))
        return render_template('add/addTutores.html', error_message=None)
    
    def agregar_licencia(self, conexion):
        if request.method == 'POST':
            employeeNumber = request.form['employeeNumber']
            fullName = request.form['fullName']
            license = request.form['license']
            licenseStar = request.form['licenseStar']
            licenseEnd = request.form['licenseEnd']        
            licenseDays = request.form['licenseDays']        
            adjustment = request.form['adjustment']
            connection = conexion.connect()
            cursor = connection.cursor()        
            insert_query = """
                INSERT INTO tec_licencesSpecialReports (
                    employeeNumber, 
                    fullName, 
                    license, 
                    licenseStar, 
                    licenseEnd, 
                    licenseDays, 
                    adjustment
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, employeeNumber, fullName, license, licenseStar, licenseEnd, licenseDays, adjustment)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('licencias_especiales'))
        return render_template('add/addLicencias.html', error_message=None)
    
    
    
    
    
    
    
    
    
    