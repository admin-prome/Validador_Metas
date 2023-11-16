from flask import Flask, redirect, render_template, request, send_file, session, url_for, jsonify
from models.views import *

vistas = Vistas()

class Login():
    def inicio(self, conexion):
        usuario = session.get('usuario')    
        if usuario:
            perfil, nombre = vistas.perfil_index(conexion, usuario['mail'])
            return render_template('index.html', nombre=nombre, perfil=perfil)
        else:
            return redirect(url_for('login'))
    
    def logger(self, conexion):
        if request.method == 'POST':
            mail = request.form['mail']
            passw = request.form['passw']
            connection = conexion.connect()
            cursor = connection.cursor()
            select_query = "SELECT * FROM tec_usersVM WHERE mail = ?"
            cursor.execute(select_query, mail)
            user = cursor.fetchone()
            cursor.close()
            if user is None:
                session['error_message'] = 'Correo electrónico no encontrado'
                return render_template('not_authorized.html')
            if user:
                if user.passw == passw:
                    session['usuario'] = {
                        'id': user.id,
                        'employeeNumber': user.employeeNumber,
                        'fullName': user.fullName,
                        'mail': user.mail,
                        'perfil': user.perfil
                    }
                    return redirect(url_for('index'))
                else:
                    session['error_message'] = 'La contraseña es incorrecta'
                    return redirect(url_for('login'))
            else:
                session['error_message'] = 'Correo electrónico no encontrado'
                return redirect(url_for('login'))
        error_message = session.pop('error_message', None)
        return render_template('login.html', error_message=error_message)
    
    def logout(self):
        session.pop('usuario', None)
        return redirect(url_for('login'))
    
    
    