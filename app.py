import os
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, request, send_file, session, url_for, jsonify
from dotenv import load_dotenv
from db.conection import DatabaseConnection
from utils.add_nomina import *
from utils.profile import *
from utils.update_nomina import *
from export.export_data import *
from models.views import *
from models.edit import *
from models.delete import *
from models.add import *
from models.export import *
from models.login import *
from models.ajustes import *
import pandas as pd


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
CONEC = DatabaseConnection()
vistas = Vistas()
edition = Edit()
delete = Eliminar()
add = Agregar()
export = ExportExcel()
logger = Login()
ajustes = Settings()
app = Flask(__name__, static_folder='public')
app.secret_key = 'tu_clave_secreta'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# TODO----------LOGIN--------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    return logger.logger(CONEC)

@app.route('/logout', methods=['POST'])
def logout():
    return logger.logout()

@app.route('/index', methods=['GET', 'POST'])
def index():
    return logger.inicio(CONEC)        

# TODO----------NOMINA-------------------------------------------------------------------------------------------------
@app.route('/nomina', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas', 'Jefe Zonal', 'Jefe Coordinador'])
def nomina():
    return vistas.vista_nomina(CONEC)

@app.route('/edit_observacion/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas', 'Jefe Zonal', 'Jefe Coordinador'])
def edit_observacion(legajo):
    if request.method == 'POST':
        nueva_observacion = request.form.get('Observacion')
        edition.actualizar_observacion(CONEC, legajo, nueva_observacion)
        return redirect(url_for('nomina'))
    observacion = vistas.obtener_observacion(CONEC,legajo)    
    return render_template('edit/editObservacion.html', legajo=legajo, fullName=observacion[0], observacion=observacion[1])

@app.route('/delete_observacion', methods=['POST'])
@profile_required(['Admin', 'Personas', 'Jefe Zonal', 'Jefe Coordinador'])
def delete_observacion():
    return delete.delete_observacion(CONEC)

@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    import time
    time.sleep(2)
    return jsonify({'success': True})

@app.route('/update-datos', methods=['POST'])
def update_datos():
    return ajustes.update_datos(CONEC)

# TODO----------Licencias-------------------------------------------------------------------------------------------------
@app.route('/licencias', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas'])
def licencias():
    licencias = vistas.obtener_licencias(CONEC)
    return render_template('licencias.html', licencias=licencias)

# TODO-----------METAS------------------------------------------------------------------------------------------------
@app.route('/metas', methods=['GET', 'POST'])
@profile_required(['Admin', 'Inteligencia Comercial'])
def metas():
    metas = vistas.obtener_metas(CONEC)
    return render_template('metas.html', metas=metas)

@app.route('/editar-meta/<categoria>', methods=['GET', 'POST'])
@profile_required(['Admin','Inteligencia Comercial'])
def editar_meta(categoria):    
    return edition.editar_meta(CONEC, categoria)

@app.route('/eliminar-meta/<categoria>', methods=['POST'])
@profile_required(['Admin','Inteligencia Comercial'])
def eliminar_meta(categoria):
    return delete.eliminar_meta(CONEC, categoria)

@app.route('/agregar-meta', methods=['GET', 'POST'])
@profile_required(['Admin', 'Inteligencia Comercial'])
def agregar_meta():    
    return add.agregar_meta(CONEC)
            
# TODO-----------PROGRESIONES-----------------------------------------------------------------------------------------
@app.route('/progresiones', methods=['GET', 'POST'])
@profile_required(['Admin', 'Personas', 'Desarrollo de Carrera'])
def progresiones():
    progresiones = vistas.obtener_progresiones(CONEC)
    return render_template('progresiones.html', 
                           progresiones=progresiones)
    
@app.route('/editar-progresion/<categoria>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def editar_progresion(categoria):
    return edition.editar_progresion(CONEC, categoria)
    
@app.route('/eliminar-progresion/<categoria>', methods=['POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def eliminar_progresion(categoria):
    return delete.eliminar_progresion(CONEC, categoria)

@app.route('/agregar-progresion', methods=['GET', 'POST'])
@profile_required(['Admin'])
def agregar_progresion():
    return add.agregar_progresion(CONEC)

# TODO------------USERS------------------------------------------------------------------------------------------
@app.route('/users', methods=['GET', 'POST'])
@profile_required(['Admin'])
def users():
    users = vistas.obtener_users(CONEC)
    return render_template('users.html', users=users)
    
@app.route('/eliminar-user/<legajo>', methods=['POST'])
@profile_required(['Admin'])
def eliminar_user(legajo):
    return delete.eliminar_user(CONEC, legajo)
 
@app.route('/editar-usuario/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin'])
def editar_usuario(legajo):    
    return edition.editar_usuario(CONEC, legajo)
    
@app.route('/agregar-usuario', methods=['GET', 'POST'])
@profile_required(['Admin'])
def agregar_usuario():
    return add.agregar_usuario(CONEC)

# TODO-------------USUARIOS_CON_PROGRESIONES---------------------------------------------------------------------------
@app.route('/usuariosConProgresiones')
@profile_required(['Admin', 'Personas', 'Desarrollo de Carrera'])
def usuarios_con_progresion():
    usuarios = vistas.obtener_usuarios_con_progresion(CONEC)
    return render_template('usuariosConProgresiones.html', usuarios=usuarios)
    
@app.route('/editar-usuarioConProgresiones/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def editar_usuario_con_progresiones(legajo):
    return edition.editar_usuario_con_progresiones(CONEC, legajo)

@app.route('/eliminar-usuarioConProgresiones/<legajo>', methods=['POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def eliminar_usuario_con_progresiones(legajo):
    return delete.eliminar_usuario_con_progresiones(CONEC, legajo)

@app.route('/agregar-usuarioConProgresion', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def agregar_usuario_con_progresion():
    return add.agregar_usuario_con_progresion(CONEC)

# TODO-------------TUTORES------------------------------------------------------------------------------------
@app.route('/tutores')
@profile_required(['Admin', 'Personas', 'Desarrollo de Carrera'])
def tutores():
    usuarios = vistas.obtener_tutores(CONEC)
    return render_template('tutores.html', usuarios=usuarios)
    
@app.route('/editar-Tutores/<legajo>', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def editar_tutores(legajo):    
    return edition.editar_tutores(CONEC, legajo)
       
@app.route('/eliminar-tutores/<legajo>', methods=['POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def eliminar_tutores(legajo):
    return delete.eliminar_tutores(CONEC, legajo)

@app.route('/agregar-Tutor', methods=['GET', 'POST'])
@profile_required(['Admin', 'Desarrollo de Carrera'])
def agregar_tutor():
    return add.agregar_tutor(CONEC)

#TODO--------LICENCIAS ESPECIALES--------------------------------------------------------
@app.route('/licenciasEspeciales')
@profile_required(['Admin', 'Personas'])
def licencias_especiales():
    licencias = vistas.obtener_licencias_especiales(CONEC)
    return render_template('licenciasEspeciales.html', licencias=licencias)

@app.route('/editar-Licencia/<employeeNumber>', methods=['GET', 'POST'])
@profile_required(['Admin'])
def editar_licencia(employeeNumber):
    return edition.editar_licencia(CONEC, employeeNumber)
    
@app.route('/eliminar-Licencia/<employeeNumber>', methods=['POST'])
@profile_required(['Admin'])
def eliminar_licencia(employeeNumber):
    return delete.eliminar_licencia(CONEC, employeeNumber)

@app.route('/agregar-Licencia', methods=['GET', 'POST'])
@profile_required(['Admin'])
def agregar_licencia():
    return add.agregar_licencia(CONEC)

#TODO--------VALIDACION_DE_USUARIO_LOGUEADO--------------------------------------------------------
@app.before_request
def before_request():
    if request.endpoint != 'login' and 'usuario' not in session:
        return redirect(url_for('login'))

#TODO--------EXPORT_TO_EXCEL----------------------------------------------------------------------
@app.route('/export_excel', methods=['POST'])
def export_excel():
    return export.export_excel(CONEC)
    
@app.route('/export_to_excel_azure', methods=['POST'])
def export_excel_azure():
    return export.export_excel_azure(CONEC)

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
        connection = CONEC.connect()
        cursor = connection.cursor()   
        delete_query = "TRUNCATE TABLE tec_nominaAllDataVM"
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
        connection = CONEC.connect()
        cursor = connection.cursor()
        delete_query = "TRUNCATE TABLE tec_licencesReports"
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
    