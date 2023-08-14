import json
import os
from flask import Flask, redirect, render_template, request, send_file, session, url_for
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)


def export_to_excel(nomina_data):
    wb = Workbook()
    ws = wb.active
    bold_font = Font(bold=True)
    fill = PatternFill(start_color="9ACD32", end_color="9ACD32", fill_type="solid")
    columns = ["Legajo", "Nombre EC", "Mail", "Sucursal", "Categoria", "Jefe a Cargo", "meta Q Mes 1", "meta Q Mes 2", "Meta $ mes 1", "Meta $ mes 2", "Descripción Licencias", "Cant Dias Licenc", "es tutor", "Tiene Progresion", "Ajuste Q", "Ajuste Monto", "Observaciones"]
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_num, value=column_title)
        cell.font = bold_font
        cell.fill = fill
    for user in nomina_data:
        row_data = [
            user.get("legajo", ""),
            user.get("Nombre_de_EC", ""),
            user.get("mail", ""),
            user.get("Sucursal", ""),
            user.get("Categoria", ""),
            user.get("jefe_a_cargo", ""),
            get_meta_q(user.get("Categoria", "")) / 2,
            get_meta_q(user.get("Categoria", "")) / 2,
            get_meta_monto(user.get("Categoria", "")) / 2,
            get_meta_monto(user.get("Categoria", "")) / 2,
            user.get("Descripcion_Licencias", ""),
            user.get("Cant_Dias_Licencia", ""),
            is_tutor(user.get("legajo", "")),
            has_progresiones(user.get("legajo", "")),
            ajuste_meta_q(user.get("Categoria", ""), user.get("legajo", "")),
            ajuste_meta_monto(user.get("Categoria", ""), user.get("legajo", "")),
            user.get("Observaciones", "")
        ]
        ws.append(row_data)        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file_path = os.path.join(current_dir, 'data', 'export', 'nominas.xlsx')
    excel_file = excel_file_path
    wb.save(excel_file)
    return excel_file

def handle_form_submission(jefe_zonal):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_nomina = os.path.join(current_dir, 'data', 'json', 'nomina.json')
    with open(json_path_nomina, 'r') as file_nomina:
        data_metas = json.load(file_nomina)
        nomina = data_metas['Nomina']    
    filtered_nomina = [entry for entry in nomina if entry['jefe_a_cargo'] == jefe_zonal]
    return filtered_nomina

def ajuste_meta_q(categoria, legajo):
    AJUSTE_TUTORES = 0.1
    result = 0
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_metas = os.path.join(current_dir, 'data', 'json', 'metas.json')
    json_path_tutores = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    json_path_progresiones = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    json_path_progresionOfUsers = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    json_path_nomina = os.path.join(current_dir, 'data', 'json', 'nomina.json')    

    def meta_real_q(categoria):
        with open(json_path_metas, 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_q = meta['cantidad']
                return meta_q
        return 0
    
    def tutores_ec(legajo):
        with open(json_path_tutores, 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                if tutor['categoria'] == 'C-JU - EC Junior' or tutor['categoria'] == 'C-JC - EC Junior en Capacitacion':
                    return AJUSTE_TUTORES
                else:
                    return 0
        return 0
    
    def progresion_ec(categoria, legajo):
        with open(json_path_progresiones, 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open(json_path_progresionOfUsers, 'r') as file_progresionOfUsers:
            data_progresionOfUsers = json.load(file_progresionOfUsers)
            progresionOfUsers = data_progresionOfUsers['Progresion_Users']        
            for user in progresionOfUsers:
                if user['legajo'] == legajo:
                    mes_progresion = user['mes_progresion']
                    for progresion in progresiones:
                        if progresion['categoria'] == categoria:
                            ajuste = progresion[mes_progresion]
                            return ajuste
        return 0
    
    def ajuste_licencias(legajo):
        with open(json_path_nomina, 'r') as file_nomina:
            data_nomina = json.load(file_nomina)
            nomina = data_nomina['Nomina']
        for user in nomina:
            if user['legajo'] == legajo:
                Descripcion_Licencias = user['Descripcion_Licencias']
                Cant_Dias_Licencia = int(user['Cant_Dias_Licencia'])
                if Descripcion_Licencias == "3553-Vacaciones":
                    if Cant_Dias_Licencia < 14:
                        return 0
                    else:
                        return 0.15
                if Descripcion_Licencias == "4104-Licencia por Accidente":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                    
                if Descripcion_Licencias == "4110-Licencias por Enfermedad":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                    
                if Descripcion_Licencias == "4132-Licencia por Maternidad":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                    
                if Descripcion_Licencias == "4133-Período de Excedencia":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                
                return 0
        return 0

    meta_real = meta_real_q(categoria)
    ajuste_tutores = tutores_ec(legajo)
    ajuste_progresion = progresion_ec(categoria, legajo)
    ajuste_licencias = ajuste_licencias(legajo)
    ajuste_total = ajuste_tutores + ajuste_progresion + ajuste_licencias
    ajustes = 1 - ajuste_total
    if ajuste_total >= 1:
        ajustes = 0
    result = round(meta_real * ajustes)
    return result
    
def ajuste_meta_monto(categoria, legajo):
    AJUSTE_TUTORES = 0.1
    result = 0    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path_metas = os.path.join(current_dir, 'data', 'json', 'metas.json')
    json_path_tutores = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    json_path_progresiones = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    json_path_progresionOfUsers = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    json_path_nomina = os.path.join(current_dir, 'data', 'json', 'nomina.json')

    def meta_real_monto(categoria):
        with open(json_path_metas, 'r') as file_metas:
            data_metas = json.load(file_metas)
            metas = data_metas['Metas']
        for meta in metas:
            if meta['categoria'] == categoria:
                meta_monto = meta['monto']
                return meta_monto
        return 1    

    def tutores_ec(legajo):
        with open(json_path_tutores, 'r') as file_tutores:
            data_tutores = json.load(file_tutores)
            tutores = data_tutores['Tutores']
        for tutor in tutores:
            if tutor['legajo'] == legajo:
                if tutor['categoria'] == 'C-JU - EC Junior' or tutor['categoria'] == 'C-JC - EC Junior en Capacitacion':
                    return AJUSTE_TUTORES
                else:
                    return 0
        return 0

    def progresion_ec(categoria, legajo):  
        with open(json_path_progresiones, 'r') as file_progresiones:
            data_progresiones = json.load(file_progresiones)
            progresiones = data_progresiones['Progresiones']        
        with open(json_path_progresionOfUsers, 'r') as file_progresionOfUsers:
            data_progresionOfUsers = json.load(file_progresionOfUsers)
            progresionOfUsers = data_progresionOfUsers['Progresion_Users']        
            for user in progresionOfUsers:
                if user['legajo'] == legajo:
                    mes_progresion = user['mes_progresion']
                    for progresion in progresiones:
                        if progresion['categoria'] == categoria:
                            ajuste = progresion[mes_progresion]
                            return ajuste
        return 0
    
    def ajuste_licencias(legajo):
        with open(json_path_nomina, 'r') as file_nomina:
            data_nomina = json.load(file_nomina)
            nomina = data_nomina['Nomina']
        for user in nomina:
            if user['legajo'] == legajo:
                Descripcion_Licencias = user['Descripcion_Licencias']
                Cant_Dias_Licencia = int(user['Cant_Dias_Licencia'])
                if Descripcion_Licencias == "3553-Vacaciones":
                    if Cant_Dias_Licencia < 14:
                        return 0
                    else:
                        return 0.15
                if Descripcion_Licencias == "4104-Licencia por Accidente":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                    
                if Descripcion_Licencias == "4110-Licencias por Enfermedad":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                    
                if Descripcion_Licencias == "4132-Licencia por Maternidad":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                    
                if Descripcion_Licencias == "4133-Período de Excedencia":
                    if Cant_Dias_Licencia > 10:
                        return 1.0                
                return 0
        return 0

    meta_real = meta_real_monto(categoria)
    ajuste_tutores = tutores_ec(legajo)
    ajuste_progresion = progresion_ec(categoria, legajo)
    ajuste_licencias = ajuste_licencias(legajo)
    ajuste_total = ajuste_tutores + ajuste_progresion + ajuste_licencias
    ajustes = 1 - ajuste_total
    if ajuste_total >= 1:
        ajustes = 0
    result = meta_real * ajustes
    return result

def get_meta_q(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return meta['cantidad']
    return "0"

def get_meta_monto(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return meta['monto']
    return "0"

def read_tutores():
    with open('data/json/tutores.json') as file_tutores:
        data_tutores = json.load(file_tutores)
    result = []
    for obj in data_tutores['Tutores']:
        result.append(obj)
        legajo = obj['legajo']
        # print(legajo)
    return result

def read_progresiones():
    with open('data/json/progresionOfUsers.json') as file_progression:
        data_progression = json.load(file_progression)
    result = []
    for obj in data_progression['Progresion_Users']:
        result.append(obj)
        legajo = obj['legajo']
        # print(legajo)
    return result

def is_tutor(legajo):
    tutores_data = read_tutores()
    tutores_legajos = [tutor['legajo'] for tutor in tutores_data]
    if legajo in tutores_legajos:
        return "SI"
    else:
        return "NO"
      
def has_progresiones(legajo):
    progresiones_data = read_progresiones() 
    legajos_con_progresiones = [progresion['legajo'] for progresion in progresiones_data]
    if legajo in legajos_con_progresiones:
        return "SI"
    else:
        return "NO"


app = Flask(__name__, static_folder='public')
app.secret_key = 'tu_clave_secreta'

# TODO----------LOGIN----------------------------------------------------------------------------------------------


@app.route('/', methods=['GET', 'POST'])
def login():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'users.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        usuarios = data['Users']    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for user in usuarios:
            if user['mail'] == email:
                if user['password'] == password:
                    session['usuario'] = user
                    return redirect(url_for('index'))
                else:
                    session['error_message'] = 'La contraseña es incorrecta'
                    return redirect(url_for('login'))        
        return render_template('not_authorized.html') 
    error_message = session.pop('error_message', None)   
    return render_template('login.html', error_message=error_message)


@app.route('/index', methods=['GET', 'POST'])
def index():
    usuario = session.get('usuario')
    if usuario:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'data', 'json', 'users.json')
        
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        usuarios = data['Users']
        perfil = next((usr['perfil'] for usr in usuarios if usr['legajo'] == usuario['legajo']), None)
        nombre = usuario['nombre']
        return render_template('index.html', nombre=nombre, perfil=perfil)
      

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


# TODO----------NOMINA-------------------------------------------------------------------------------------------------

@app.route('/nomina', methods=['GET', 'POST'])
def nomina():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'nomina.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        nomina = data["Nomina"]
    
    if request.method == 'POST':
        jefe_zonal = request.form['user']
        filtered_nomina = handle_form_submission(jefe_zonal)
        return render_template('nomina.html', nomina=filtered_nomina, is_tutor=is_tutor, has_progresiones=has_progresiones, get_meta_q=get_meta_q, get_meta_monto=get_meta_monto, ajuste_meta_q=ajuste_meta_q, ajuste_meta_monto=ajuste_meta_monto, handle_form_submission=handle_form_submission)
    else:
        return render_template('nomina.html', nomina=nomina, is_tutor=is_tutor, has_progresiones=has_progresiones, get_meta_q=get_meta_q, get_meta_monto=get_meta_monto, ajuste_meta_q=ajuste_meta_q, ajuste_meta_monto=ajuste_meta_monto, handle_form_submission=handle_form_submission)


@app.route('/edit_observacion/<legajo>', methods=['GET', 'POST'])
def edit_observacion(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'nomina.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    nomina = data['Nomina']
    usuario = next((user for user in nomina if user['legajo'] == int(legajo)), None)
    if request.method == 'POST':
        nueva_observacion = request.form.get('Observaciones')
        usuario['Observaciones'] = nueva_observacion
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return redirect(url_for('nomina'))
    
    return render_template('edit/editObservacion.html', usuario=usuario)


@app.route('/delete_observacion', methods=['POST'])
def delete_observacion():
    legajo = request.form['legajo']
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'nomina.json')

    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    
    nomina = data['Nomina']
    usuario = next((user for user in nomina if user['legajo'] == int(legajo)), None)
    if usuario:
        usuario['Observaciones'] = ""

        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
            
    return redirect('/nomina')


# TODO-----------METAS------------------------------------------------------------------------------------------------


@app.route('/metas', methods=['GET', 'POST'])
def metas():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'metas.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        metas = data["Metas"]
    return render_template('metas.html', metas=metas)


@app.route('/editar-meta/<categoria>', methods=['GET', 'POST'])
def editar_meta(categoria):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'metas.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    metas = data['Metas']
    datos_categoria = next((meta for meta in metas if meta['categoria'] == categoria), None)    
    if request.method == 'POST':
        nueva_cantidad = int(request.form.get('cantidad'))
        nuevo_monto = float(request.form.get('monto'))
        nuevo_monto_prom = float(request.form.get('monto_prom'))
        nueva_fecha = request.form.get('fecha')
        datos_categoria['cantidad'] = nueva_cantidad
        datos_categoria['monto'] = nuevo_monto
        datos_categoria['monto_prom'] = nuevo_monto_prom
        datos_categoria['fecha'] = nueva_fecha        
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)        
        return redirect(url_for('metas'))
    return render_template('edit/editMetas.html', datos_categoria=datos_categoria)


@app.route('/eliminar-meta/<categoria>', methods=['POST'])
def eliminar_meta(categoria):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'metas.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    metas = data['Metas']
    meta_a_eliminar = None
    for meta in metas:
        if meta['categoria'] == categoria:
            meta_a_eliminar = meta
            break
    if meta_a_eliminar:
        metas.remove(meta_a_eliminar)
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    return redirect(url_for('metas'))


@app.route('/agregar-meta', methods=['GET', 'POST'])
def agregar_meta():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'metas.json')    
    if request.method == 'POST':
        categoria = request.form['categoria']
        cantidad = int(request.form['cantidad'])
        monto = float(request.form['monto'])
        monto_prom = float(request.form['monto_prom'])
        fecha = request.form['fecha']        
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
            metas = data['Metas']
            # Validar si la categoría ya existe en el archivo JSON
        if any(meta['categoria'] == categoria for meta in metas):
            error_message = 'La categoría ya existe. No se permite agregar una meta con la misma categoría.'
            return render_template('add/addMetas.html', error_message=error_message)        
        nueva_meta = {
            'categoria': categoria,
            'cantidad': cantidad,
            'monto': monto,
            'monto_prom': monto_prom,
            'fecha': fecha
        }        
        metas.append(nueva_meta)        
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)        
        return redirect(url_for('metas'))    
    return render_template('add/addMetas.html')


# TODO-----------PROGRESIONES-----------------------------------------------------------------------------------------


@app.route('/progresiones', methods=['GET', 'POST'])
def progresiones():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresiones.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        progresiones = data["Progresiones"]
    return render_template('progresiones.html', progresiones=progresiones)


@app.route('/editar-progresion/<categoria>', methods=['GET', 'POST'])
def editar_progresion(categoria):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresiones.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    progresiones = data['Progresiones']
    datos_progresion = next((progresion for progresion in progresiones if progresion['categoria'] == categoria), None)    
    if request.method == 'POST':
        datos_progresion['mes_1'] = float(request.form.get('mes_1'))
        datos_progresion['mes_2'] = float(request.form.get('mes_2'))
        datos_progresion['mes_3'] = float(request.form.get('mes_3'))
        datos_progresion['mes_4'] = float(request.form.get('mes_4'))
        datos_progresion['mes_5'] = float(request.form.get('mes_5'))
        datos_progresion['mes_6'] = float(request.form.get('mes_6'))              
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)        
        return redirect(url_for('progresiones'))
    return render_template('edit/editProgresiones.html', datos_progresion=datos_progresion)


@app.route('/eliminar-progresion/<categoria>', methods=['POST'])
def eliminar_progresion(categoria):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresiones.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    progresiones = data['Progresiones']
    progresion_a_eliminar = None
    for progresion in progresiones:
        if progresion['categoria'] == categoria:
            progresion_a_eliminar = progresion
            break
    if progresion_a_eliminar:
        progresiones.remove(progresion_a_eliminar)
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    return redirect(url_for('progresiones'))


@app.route('/agregar-progresion', methods=['GET', 'POST'])
def agregar_progresion():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresiones.json')    
    if request.method == 'POST':
        categoria = request.form['categoria']
        mes_1 = float(request.form['mes_1'])
        mes_2 = float(request.form['mes_2'])
        mes_3 = float(request.form['mes_3'])
        mes_4 = float(request.form['mes_4'])
        mes_5 = float(request.form['mes_5'])
        mes_6 = float(request.form['mes_6'])        
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
            progresiones = data['Progresiones']        
        # Validar si la categoría ya existe en el archivo JSON
        if any(progresion['categoria'] == categoria for progresion in progresiones):
            error_message = 'La categoría ya existe. No se permite agregar otra progresion con la misma categoría.'
            return render_template('add/addMetas.html', error_message=error_message)       
        nueva_progresion = {
            'categoria': categoria,
            'mes_1': mes_1,
            'mes_2': mes_2,
            'mes_3': mes_3,
            'mes_4': mes_4,
            'mes_5': mes_5,
            'mes_6': mes_6
        }        
        progresiones.append(nueva_progresion)        
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)        
        return redirect(url_for('progresiones'))    
    return render_template('add/addProgresiones.html')


# TODO------------USERS------------------------------------------------------------------------------------------


@app.route('/users', methods=['GET', 'POST'])
def users():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'users.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        users = data["Users"]        
    selected_user = request.form.get('user')
    return render_template('users.html', users=users, selected_user=selected_user)


@app.route('/eliminar-user/<legajo>', methods=['POST'])
def eliminar_user(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'users.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    users = data['Users']    
    user_a_eliminar = None
    for user in users:
        if user['legajo'] == int(legajo):
            user_a_eliminar = user
            break        
    if user_a_eliminar:
        users.remove(user_a_eliminar)    
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)        
    return redirect(url_for('users'))    
               

@app.route('/editar-usuario/<legajo>', methods=['GET', 'POST'])
def editar_usuario(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'users.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    usuarios = data['Users']
    datos_usuario = next((usuario for usuario in usuarios if usuario['legajo'] == int(legajo)), None)    
    if request.method == 'POST':
        nuevo_apellido = request.form.get('apellido')
        nuevo_nombre = request.form.get('nombre')
        nuevo_mail = request.form.get('mail')
        nuevo_perfil = request.form.get('perfil')
        datos_usuario['apellido'] = nuevo_apellido
        datos_usuario['nombre'] = nuevo_nombre
        datos_usuario['mail'] = nuevo_mail
        datos_usuario['perfil'] = nuevo_perfil        
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)        
        return redirect(url_for('users'))
    return render_template('edit/editUsers.html', datos_usuario=datos_usuario)


@app.route('/agregar-usuario', methods=['GET', 'POST'])
def agregar_usuario():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'users.json')
    if request.method == 'POST':
        legajo = int(request.form['legajo'])
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']
        perfil = request.form['perfil']
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
            usuarios = data['Users']
        # Validar si el legajo ya existe en el archivo JSON
        if any(usuario['legajo'] == legajo for usuario in usuarios):
            error_message = 'El legajo ya existe. No se permite agregar un usuario con el mismo legajo.'
            return render_template('add/addUsers.html', error_message=error_message)
        
        nuevo_usuario = {
            'legajo': legajo,
            'nombre': nombre,
            'mail': mail,
            'password': password,
            'perfil': perfil
        }
        usuarios.append(nuevo_usuario)
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return redirect(url_for('users'))
    return render_template('add/addUsers.html')


# TODO-------------USUARIOS_CON_PROGRESIONES---------------------------------------------------------------------------


@app.route('/usuariosConProgresiones')
def usuarios_con_progresion():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        usuarios = data['Progresion_Users']
    return render_template('usuariosConProgresiones.html', usuarios=usuarios)


@app.route('/editar-usuarioConProgresiones/<legajo>', methods=['GET', 'POST'])
def editar_usuario_con_progresiones(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    usuarios = data["Progresion_Users"]
    datos_usuarioConProgresiones = next((usuario for usuario in usuarios if usuario['legajo'] == int(legajo)), None)
    if request.method == 'POST':
        datos_usuarioConProgresiones['apellido'] = request.form.get('apellido')
        datos_usuarioConProgresiones['nombre'] = request.form.get('nombre')
        datos_usuarioConProgresiones['mail'] = request.form.get('mail')
        datos_usuarioConProgresiones['categoria'] = request.form.get('categoria')
        datos_usuarioConProgresiones['fecha_desde'] = request.form.get('fecha_desde')
        datos_usuarioConProgresiones['fecha_hasta'] = request.form.get('fecha_hasta')
        datos_usuarioConProgresiones['mes_progresion'] = request.form.get('mes_progresion')
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return redirect(url_for('usuarios_con_progresion'))
    return render_template('edit/editUsuariosConProgresiones.html', datos_usuarioConProgresiones=datos_usuarioConProgresiones)


@app.route('/eliminar-usuarioConProgresiones/<legajo>', methods=['POST'])
def eliminar_usuario_con_progresiones(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    usuarios = data['Progresion_Users']
    usuario_a_eliminar = next((usuario for usuario in usuarios if usuario['legajo'] == int(legajo)), None)
    if usuario_a_eliminar:
        usuarios.remove(usuario_a_eliminar)
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
    return redirect(url_for('usuarios_con_progresion'))


@app.route('/agregar-usuarioConProgresion', methods=['GET', 'POST'])
def agregar_usuario_con_progresion():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'progresionOfUsers.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        usuarios = data['Progresion_Users']
    if request.method == 'POST':
        legajo = int(request.form.get('legajo'))
        
        # Validar si el legajo ya existe en el archivo JSON
        if any(usuario['legajo'] == legajo for usuario in usuarios):
            error_message = 'El legajo ya existe. No se permite agregar un usuario con el mismo legajo.'
            return render_template('add/addUsuarioConProgresion.html', error_message=error_message)
        
        nuevo_usuario = {
            'legajo': legajo,
            'apellido': request.form.get('apellido'),
            'nombre': request.form.get('nombre'),
            'mail': request.form.get('mail'),
            'categoria': request.form.get('categoria'),
            'fecha_desde': request.form.get('fecha_desde'),
            'fecha_hasta': request.form.get('fecha_hasta'),
            'mes_progresion': request.form.get('mes_progresion')
        }
        usuarios.append(nuevo_usuario)
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return redirect(url_for('usuarios_con_progresion'))
    return render_template('add/addUsuarioConProgresion.html', error_message=None)


# TODO-------------TUTORES------------------------------------------------------------------------------------


@app.route('/tutores')
def tutores():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        usuarios = data['Tutores']
    return render_template('tutores.html', usuarios=usuarios)


@app.route('/editar-Tutores/<legajo>', methods=['GET', 'POST'])
def editar_tutores(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        usuarios = data['Tutores']
    datos_tutores = next((usuario for usuario in usuarios if usuario['legajo'] == int(legajo)), None)
    if request.method == 'POST':
        datos_tutores['nombre'] = request.form.get('nombre')
        datos_tutores['apellido'] = request.form.get('apellido')
        datos_tutores['categoria'] = request.form.get('categoria')
        datos_tutores['fecha_inicio_tutoria'] = request.form.get('fecha_inicio_tutoria')
        datos_tutores['fecha_fin_tutoria'] = request.form.get('fecha_fin_tutoria')
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return redirect(url_for('tutores'))
    return render_template('edit/editTutores.html', datos_tutores=datos_tutores)
       
    
@app.route('/eliminar-tutores/<legajo>', methods=['POST'])
def eliminar_tutores(legajo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    usuarios = data['Tutores']
    tutor_a_eliminar = next((usuario for usuario in usuarios if usuario['legajo'] == int(legajo)), None)
    if tutor_a_eliminar:
        usuarios.remove(tutor_a_eliminar)
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
    return redirect(url_for('tutores'))


@app.route('/agregar-Tutor', methods=['GET', 'POST'])
def agregar_tutor():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'tutores.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        tutores = data['Tutores']
    if request.method == 'POST':
        legajo = int(request.form.get('legajo'))       
        # Validar si el legajo ya existe en el archivo JSON
        if any(tutor['legajo'] == legajo for tutor in tutores):
            error_message = 'El legajo ya existe. No se permite agregar un tutor con el mismo legajo.'
            return render_template('add/addTutores.html', error_message=error_message)        
        nuevo_tutor = {
            'legajo': legajo,
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'categoria': request.form.get('categoria'),
            'fecha_inicio_tutoria': request.form.get('fecha_inicio_tutoria'),
            'fecha_fin_tutoria': request.form.get('fecha_fin_tutoria')
        }
        tutores.append(nuevo_tutor)
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return redirect(url_for('tutores'))
    return render_template('add/addTutores.html', error_message=None)


#TODO--------VALIDACION_DE_USUARIO_LOGUEADO--------------------------------------------------------


@app.before_request
def before_request():
    if request.endpoint != 'login' and 'usuario' not in session:
        return redirect(url_for('login'))


#TODO--------EXPORT_TO_EXCEL----------------------------------------------------------------------


@app.route('/export_excel', methods=['POST'])
def export_excel():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'json', 'nomina.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        nomina = data["Nomina"]
    
    excel_file = export_to_excel(nomina)
    return send_file(excel_file, as_attachment=True)


if __name__ == '__main__':    
    app.run()
    