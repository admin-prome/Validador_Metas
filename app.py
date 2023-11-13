import os
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, request, send_file, session, url_for, jsonify
from dotenv import load_dotenv
from db.conection import DatabaseConnection
from utils.add_nomina import *
from utils.profile import *
from utils.update_nomina import *
from export.export_data import *
import pandas as pd


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)


app = Flask(__name__, static_folder='public')
app.secret_key = 'tu_clave_secreta'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# TODO----------LOGIN--------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        passw = request.form['passw']
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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

@app.route('/index', methods=['GET', 'POST'])
def index():
    usuario = session.get('usuario')    
    if usuario:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query = "SELECT perfil, fullName FROM tec_usersVM WHERE mail = ?"
        cursor.execute(select_query, usuario['mail'])
        result = cursor.fetchone()
        cursor.close()
        if result:
            perfil = result[0] 
            nombre = result[1]
        else:
            perfil, nombre = None, None
        actualizar_datos()        
        return render_template('index.html', nombre=nombre, perfil=perfil)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


# TODO----------NOMINA-------------------------------------------------------------------------------------------------
@app.route('/nomina', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas', 'Jefe Zonal', 'Jefe Coordinador'])
def nomina():    
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_nominaAllDataVM"
    cursor.execute(select_query)
    nomina = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('nomina.html', 
                            nomina=nomina)

@app.route('/edit_observacion/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas', 'Jefe Zonal', 'Jefe Coordinador'])
def edit_observacion(legajo):
    if request.method == 'POST':
        nueva_observacion = request.form.get('Observacion')
        db_connection = DatabaseConnection()
        try:
            connection = db_connection.connect()
            cursor = connection.cursor()
            update_query = "UPDATE tec_nominaAllDataVM SET Observacion = ? WHERE employeeNumber = ?"
            cursor.execute(update_query, (nueva_observacion, legajo))
            connection.commit()
            return redirect(url_for('nomina'))
        except Exception as e:
            print(f'Error al editar Observacion en la base de datos: {str(e)}')
        finally:
            cursor.close()
            connection.close()
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT fullName, Observacion FROM tec_nominaAllDataVM WHERE employeeNumber = ?"
    cursor.execute(select_query, (legajo,))
    observacion = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit/editObservacion.html', 
                           legajo=legajo,
                           fullName=observacion[0],
                           observacion=observacion[1])

@app.route('/delete_observacion', methods=['POST'])
@profile_required(['Admin', 'Personas', 'Jefe Zonal', 'Jefe Coordinador'])
def delete_observacion():
    legajo = request.form.get('employeeNumber')
    if legajo is not None and legajo.isnumeric():
        db_connection = DatabaseConnection()
        try:
            connection = db_connection.connect()
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


@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    import time
    time.sleep(2)
    return jsonify({'success': True})

@app.route('/update-datos', methods=['POST'])
def update_datos():
    actualizar_datos()
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    legajo_query = """
            SELECT employeeNumber FROM tec_licencesReports
            UNION
            SELECT employeeNumber FROM tec_licencesSpecialReports
            UNION
            SELECT employeeNumber FROM tec_tutoresVM
            UNION
            SELECT employeeNumber FROM tec_progretionOfUsers;
    """
    cursor.execute(legajo_query)
    legajos = cursor.fetchall()
    for legajo in legajos:
        ajustes_metas(legajo[0])
    cursor.close()
    connection.close()
    return redirect(url_for('nomina'))

# TODO----------Licencias-------------------------------------------------------------------------------------------------
@app.route('/licencias', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas'])
def licencias():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_licencesReports"
    cursor.execute(select_query)
    licencias = cursor.fetchall()
    cursor.close()
    connection.close()
    actualizar_datos()
    return render_template('licencias.html', 
                           licencias=licencias)


# TODO-----------METAS------------------------------------------------------------------------------------------------
@app.route('/metas', methods=['GET', 'POST'])
@profile_required(['Admin', 'Inteligencia Comercial'])
def metas():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_metasVM"
    cursor.execute(select_query)
    metas = cursor.fetchall()
    cursor.close()
    connection.close()
    actualizar_datos()
    return render_template('metas.html', 
                            metas=metas)

@app.route('/editar-meta/<categoria>', methods=['GET', 'POST'])
@profile_required(['Admin','Inteligencia Comercial'])
def editar_meta(categoria):    
    if request.method == 'POST':
        nueva_cantidad = int(request.form.get('cantidad'))
        nuevo_monto = float(request.form.get('monto'))
        nuevo_monto_prom = float(request.form.get('monto_prom'))
        nueva_fecha = request.form.get('fecha')
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tec_metasVM WHERE category = ?", categoria)
    datos_categoria = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit/editMetas.html', datos_categoria=datos_categoria)

@app.route('/eliminar-meta/<categoria>', methods=['POST'])
@profile_required(['Admin','Inteligencia Comercial'])
def eliminar_meta(categoria):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_metasVM WHERE category = ?"
        cursor.execute(delete_query, categoria)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('metas'))
    except Exception as e:
        return f'Error al eliminar la meta: {str(e)}'

@app.route('/agregar-meta', methods=['GET', 'POST'])
@profile_required(['Admin', 'Inteligencia Comercial'])
def agregar_meta():    
    if request.method == 'POST':
        categoria = request.form['categoria']
        cantidad = int(request.form['cantidad'])
        monto = float(request.form['monto'])
        monto_prom = float(request.form['monto_prom'])
        fecha = request.form['fecha']        
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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
            

# TODO-----------PROGRESIONES-----------------------------------------------------------------------------------------
@app.route('/progresiones', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas', 'Desarrollo de Carrera'])
def progresiones():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_progretionVM"
    cursor.execute(select_query)
    progresiones = cursor.fetchall()
    cursor.close()
    connection.close()
    actualizar_datos()
    return render_template('progresiones.html', 
                           progresiones=progresiones)
    
@app.route('/editar-progresion/<categoria>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def editar_progresion(categoria):
    if request.method == 'POST':
        datos_progresion_1 = float(request.form.get('month_1'))
        datos_progresion_2 = float(request.form.get('month_2'))
        datos_progresion_3 = float(request.form.get('month_3'))
        datos_progresion_4 = float(request.form.get('month_4'))
        datos_progresion_5 = float(request.form.get('month_5'))
        datos_progresion_6 = float(request.form.get('month_6'))              
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()        
        update_query = "UPDATE tec_progretionVM SET month_1 = ?, month_2 = ?, month_3 = ?, month_4 = ?, month_5 = ?, month_6 = ? WHERE category = ?"
        cursor.execute(update_query, datos_progresion_1, datos_progresion_2, datos_progresion_3, datos_progresion_4, datos_progresion_5, datos_progresion_6, categoria)
        connection.commit()
        return redirect(url_for('progresiones'))
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tec_progretionVM WHERE category = ?", categoria)
    datos_progresion = cursor.fetchone()
    cursor.close()
    connection.close()    
    return render_template('edit/editProgresiones.html', 
                           datos_progresion=datos_progresion)
    
@app.route('/eliminar-progresion/<categoria>', methods=['POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def eliminar_progresion(categoria):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_progretionVM WHERE category = ?"
        cursor.execute(delete_query, categoria)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('progresiones'))
    except Exception as e:
        return f'Error al eliminar la progresion: {str(e)}'

@app.route('/agregar-progresion', methods=['GET', 'POST'])
@profile_required(['Admin'])
def agregar_progresion():
    if request.method == 'POST':
        categoria = request.form['categoria']
        month_1 = float(request.form['month_1'])
        month_2 = float(request.form['month_2'])
        month_3 = float(request.form['month_3'])
        month_4 = float(request.form['month_4'])
        month_5 = float(request.form['month_5'])
        month_6 = float(request.form['month_6'])        
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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


# TODO------------USERS------------------------------------------------------------------------------------------
@app.route('/users', methods=['GET', 'POST'])
@profile_required(['Admin'])
def users():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_usersVM"
    cursor.execute(select_query)
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('users.html', 
                           users=users)
    
@app.route('/eliminar-user/<legajo>', methods=['POST'])
@profile_required(['Admin'])
def eliminar_user(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_usersVM WHERE employeeNumber = ?"
        cursor.execute(delete_query, legajo)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('users'))   
    except Exception as e:
        return f'Error al eliminar la meta: {str(e)}'
 
@app.route('/editar-usuario/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin'])
def editar_usuario(legajo):    
    if request.method == 'POST':
        fullName = request.form['fullName']
        mail = request.form['mail']
        passw = request.form['passw']
        perfil = request.form['perfil']  
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tec_usersVM WHERE employeeNumber = ?", legajo)
    datos_usuario = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit/editUsers.html',
                           datos_usuario=datos_usuario)
    
@app.route('/agregar-usuario', methods=['GET', 'POST'])
@profile_required(['Admin'])
def agregar_usuario():
    if request.method == 'POST':
        employeeNumber = int(request.form['employeeNumber'])
        fullName = request.form['fullName']
        mail = request.form['mail']
        passw = request.form['passw']
        perfil = request.form['perfil']
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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


# TODO-------------USUARIOS_CON_PROGRESIONES---------------------------------------------------------------------------
@app.route('/usuariosConProgresiones')
@profile_required(['Admin', 'Personas', 'Desarrollo de Carrera'])
def usuarios_con_progresion():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_progretionOfUsers"
    cursor.execute(select_query)
    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()
    actualizar_datos()
    return render_template('usuariosConProgresiones.html', 
                           usuarios=usuarios)
    
@app.route('/editar-usuarioConProgresiones/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def editar_usuario_con_progresiones(legajo):
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        category = request.form.get('category')
        adjustment = request.form.get('adjustment')
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query = "SELECT COUNT(*) FROM tec_progretionOfUsers WHERE employeeNumber = ?"
        cursor.execute(select_query, legajo)
        categoria_result = cursor.fetchone()[0]
        if categoria_result > 0:
            update_query = "UPDATE tec_progretionOfUsers SET fullName = ?, category = ?, adjustment = ? WHERE employeeNumber = ?"
            cursor.execute(update_query, fullName, category, adjustment, legajo)
            connection.commit()
            ajustes_metas(legajo)
        else:
            connection.close()
            return "La categoría no existe y no se puede editar."
        return redirect(url_for('usuarios_con_progresion'))
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tec_progretionOfUsers WHERE employeeNumber = ?", legajo)
    datos_usuarioConProgresiones = cursor.fetchone()
    cursor.close()
    connection.close()            
    return render_template('edit/editUsuariosConProgresiones.html', 
                           datos_usuarioConProgresiones=datos_usuarioConProgresiones)

@app.route('/eliminar-usuarioConProgresiones/<legajo>', methods=['POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def eliminar_usuario_con_progresiones(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_progretionOfUsers WHERE employeeNumber = ?"
        cursor.execute(delete_query, legajo)
        connection.commit()
        cursor.close()
        connection.close()
        ajustes_metas(legajo)
        return redirect(url_for('usuarios_con_progresion'))
    except Exception as e:
        return f'Error al eliminar la meta: {str(e)}'

@app.route('/agregar-usuarioConProgresion', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def agregar_usuario_con_progresion():
    if request.method == 'POST':
        employeeNumber = int(request.form['employeeNumber'])
        fullName = request.form['fullName']
        category = request.form['category']
        adjustment = float(request.form['adjustment'])
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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
            ajustes_metas(employeeNumber)
        return redirect(url_for('usuarios_con_progresion'))
    return render_template('add/addUsuarioConProgresion.html', 
                           error_message=None)


# TODO-------------TUTORES------------------------------------------------------------------------------------
@app.route('/tutores')
@profile_required(['Admin', 'Personas', 'Desarrollo de Carrera'])
def tutores():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_tutoresVM"
    cursor.execute(select_query)
    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()
    actualizar_datos()
    return render_template('tutores.html', 
                           usuarios=usuarios)
    
@app.route('/editar-Tutores/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def editar_tutores(legajo):    
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        category = request.form.get('category')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        adjustment = float(request.form.get('adjustment'))
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        select_query = "SELECT COUNT(*) FROM tec_tutoresVM WHERE employeeNumber = ?"
        cursor.execute(select_query, legajo)
        categoria_result = cursor.fetchone()[0]
        if categoria_result > 0:
            update_query = "UPDATE tec_tutoresVM SET fullName = ?, category = ?, startDate = ?, endDate = ?, adjustment = ? WHERE employeeNumber = ?"
            cursor.execute(update_query, fullName, category, startDate, endDate, adjustment, legajo)
            connection.commit()
            ajustes_metas(legajo)
        else:
            connection.close()
            return "La categoría no existe y no se puede editar."
        return redirect(url_for('tutores'))
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tec_tutoresVM WHERE employeeNumber = ?", legajo)
    datos_tutores = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit/editTutores.html', 
                           datos_tutores=datos_tutores)
       
@app.route('/eliminar-tutores/<legajo>', methods=['POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def eliminar_tutores(legajo):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_tutoresVM WHERE employeeNumber = ?"
        cursor.execute(delete_query, legajo)
        connection.commit()
        cursor.close()
        connection.close()
        ajustes_metas(legajo)
        return redirect(url_for('tutores'))
    except Exception as e:
        return f'Error al eliminar la meta: {str(e)}'

@app.route('/agregar-Tutor', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def agregar_tutor():
    if request.method == 'POST':
        employeeNumber = int(request.form['employeeNumber'])       
        fullName = request.form['fullName']      
        category = request.form['category']     
        startDate = request.form['startDate']       
        endDate = request.form['endDate']      
        adjustment = float(request.form['adjustment'])
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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
            ajustes_metas(employeeNumber)
        return redirect(url_for('tutores'))
    return render_template('add/addTutores.html',
                           error_message=None)


#TODO--------LICENCIAS ESPECIALES--------------------------------------------------------
@app.route('/licenciasEspeciales')
@profile_required(['Admin', 'Personas'])
def licencias_especiales():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM tec_licencesSpecialReports"
    cursor.execute(select_query)
    licencias = cursor.fetchall()
    cursor.close()
    connection.close()
    actualizar_datos()
    return render_template('licenciasEspeciales.html', 
                           licencias=licencias)

@app.route('/editar-Licencia/<employeeNumber>', methods=['GET', 'POST'])
@profile_required(['Admin'])
def editar_licencia(employeeNumber):
    if request.method == 'POST':
        nuevo_fullName = request.form['fullName']
        nuevo_license = request.form['license']
        nuevo_licenseStar = request.form['licenseStar']
        nuevo_licenseEnd = request.form['licenseEnd']        
        nuevo_licenseDays = request.form['licenseDays']        
        nuevo_adjustment = request.form['adjustment']        
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()        
        update_query = "UPDATE tec_licencesSpecialReports SET fullName = ?, license = ?, licenseStar = ?, licenseEnd = ?, licenseDays = ?, adjustment = ? WHERE employeeNumber = ?"
        cursor.execute(update_query, nuevo_fullName, nuevo_license, nuevo_licenseStar, nuevo_licenseEnd, nuevo_licenseDays, nuevo_adjustment, employeeNumber)
        connection.commit()
        ajustes_metas(employeeNumber)
        return redirect(url_for('licencias_especiales'))
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tec_licencesSpecialReports WHERE employeeNumber = ?", employeeNumber)
    datos_licencia = cursor.fetchone()
    cursor.close()
    connection.close()    
    return render_template('edit/editLicencias.html', 
                           datos_licencia=datos_licencia)
    
@app.route('/eliminar-Licencia/<employeeNumber>', methods=['POST'])
@profile_required(['Admin'])
def eliminar_licencia(employeeNumber):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_licencesSpecialReports WHERE employeeNumber = ?"
        cursor.execute(delete_query, employeeNumber)
        connection.commit()
        cursor.close()
        connection.close()
        ajustes_metas(employeeNumber)
        return redirect(url_for('licencias_especiales'))
    except Exception as e:
        return f'Error al eliminar la meta: {str(e)}'

@app.route('/agregar-Licencia', methods=['GET', 'POST'])
@profile_required(['Admin'])
def agregar_licencia():
    if request.method == 'POST':
        employeeNumber = request.form['employeeNumber']
        fullName = request.form['fullName']
        license = request.form['license']
        licenseStar = request.form['licenseStar']
        licenseEnd = request.form['licenseEnd']        
        licenseDays = request.form['licenseDays']        
        adjustment = request.form['adjustment']        
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
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
        ajustes_metas(employeeNumber)
        return redirect(url_for('licencias_especiales'))
    return render_template('add/addLicencias.html', 
                           error_message=None)


#TODO--------VALIDACION_DE_USUARIO_LOGUEADO--------------------------------------------------------
@app.before_request
def before_request():
    if request.endpoint != 'login' and 'usuario' not in session:
        return redirect(url_for('login'))


#TODO--------EXPORT_TO_EXCEL----------------------------------------------------------------------
@app.route('/export_excel', methods=['POST'])
def export_excel():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
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
    return send_file(excel_file, 
                    as_attachment=True)
    
@app.route('/export_to_excel_azure', methods=['POST'])
def export_excel_azure():
    db_connection = DatabaseConnection()
    connection = db_connection.connect()
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


#TODO--------upload_nomina------------------------------------------------------------------------------
@app.route('/importar_nomina', methods=['GET', 'POST'])
@profile_required(['Admin'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)        
        file = request.files['file']        
        if file.filename == '':
            return redirect(request.url)        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))    
    return render_template('upload.html')

@app.route('/uploads/<filename>')
@profile_required(['Admin'])
def uploaded_file(filename):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()   
        delete_query = "DELETE FROM tec_nominaAllDataVM"
        cursor.execute(delete_query)
        connection.commit() 
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return 'El archivo no existe.'
        df = pd.read_excel(file_path)
        data_to_insert = []
        for _, row in df.iterrows():
            data = (
                row['employeeNumber'],
                row['fullName'],
                row['branch'],
                row['category'],
                '',  # Observacion
                0.0,  # metas_q
                0,  # metas_monto
                '',  # descripcion_licencias
                '',  # dias_licencias
                '',  # licencias_especiales
                '',  # dias_licencias_especiales
                '',  # es_tutor
                '',  # tiene_progresion
                0.0,  # ajuste_q_mes_uno
                0,  # ajuste_monto_mes_uno
                0.0,  # ajuste_q_mes_dos
                0,  # ajuste_monto_mes_dos
                0.0,  # ajuste_total_q
                0  # ajuste_total_monto
            )
            data_to_insert.append(data)
        try:
            insert_query = """
            INSERT INTO tec_nominaAllDataVM (  
                    employeeNumber, 
                    fullName, 
                    branch, 
                    category, 
                    Observacion, 
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
                    ajuste_total_monto
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
            for _, row in df.iterrows():
                legajo = row['employeeNumber']
            actualizar_datos()
            ajustes_metas(legajo)
        except Exception as e:
            connection.rollback()
            flash(f'Error al insertar datos en la base de datos: {str(e)}', 'danger')
            return render_template('upload.html')
        finally:
            cursor.close()
            connection.close()
    except Exception as err:
        flash(f'Error al insertar datos en la base de datos: {str(err)}', 'danger')
        return render_template('upload.html')
    flash('Archivo importado y procesado con exito', 'info')
    return render_template('ok.html')


#TODO--------upload_licencias------------------------------------------------------------------------------
@app.route('/importar_licencia', methods=['GET', 'POST'])
@profile_required(['Admin'])
def upload_licencia_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_licencia_file', 
                                    filename=filename))
    return render_template('upload_licencia.html')

@app.route('/uploads_licencia/<filename>')
@profile_required(['Admin'])
def uploaded_licencia_file(filename):
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
        delete_query = "DELETE FROM tec_licencesReports"
        cursor.execute(delete_query)
        connection.commit()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return 'El archivo no existe.'
        df = pd.read_excel(file_path)
        data_to_insert = []
        for _, row in df.iterrows():
            data = (
                row['employeeNumber'],
                row['fullName'],
                row['descriptions'],
                row['startDay'],
                row['endDay'],
                row['filterDays'],
                row['licenseDays']
            )
            data_to_insert.append(data)
        try:
            insert_query = """
            INSERT INTO tec_licencesReports (
                            employeeNumber, 
                            fullName, 
                            descriptions, 
                            startDay, 
                            endDay, 
                            filterDays, 
                            licenseDays
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
            legajo_query = """
                    SELECT employeeNumber FROM tec_licencesReports
                    UNION
                    SELECT employeeNumber FROM tec_licencesSpecialReports
                    UNION
                    SELECT employeeNumber FROM tec_tutoresVM
                    UNION
                    SELECT employeeNumber FROM tec_progretionOfUsers;
            """
            cursor.execute(legajo_query)
            legajos = cursor.fetchall()
            for legajo in legajos:
                ajustes_metas(legajo[0])
            
            actualizar_datos()
        except Exception as e:
            connection.rollback()
            return f'Error al insertar datos en la base de datos: {str(e)}'
        finally:
            cursor.close()
            connection.close()
            flash('Archivo importado y procesado con exito', 'info')
    except Exception as err:
        flash(f'Error al insertar datos en la base de datos: {str(err)}', 'danger')
        return render_template('upload_licencia.html')
    return render_template('ok.html')


if __name__ == '__main__':    
    app.run()