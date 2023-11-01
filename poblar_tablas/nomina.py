import json
from db.conection import DatabaseConnection
import pandas as pd
import numpy as np

conexion = DatabaseConnection()
csv_filename = 'datos_nomina.csv'
json_file = 'data/json/nomina.json'


def get_existing_employee_numbers(connection):  # 1ero
    cursor = connection.cursor()
    cursor.execute("SELECT employeeNumber FROM dbo.tec_payrollVM")
    result = cursor.fetchall()
    existing_numbers = [str(row.employeeNumber) for row in result]
    return existing_numbers


def insert_data_from_csv(csv_file, db_connection):  #  2do
    df = pd.read_csv(csv_file)
    connection = db_connection.connect()
    cursor = connection.cursor()    
    existing_employee_numbers = get_existing_employee_numbers(connection)    
    for index, row in df.iterrows():
        if len(row) == 4:
            employee_number = str(row['legajo'])
            if employee_number not in existing_employee_numbers:
                insert_sql = "INSERT INTO dbo.tec_payrollVM (employeeNumber, fullName, branch, category) VALUES (?, ?, ?, ?)"
                cursor.execute(insert_sql, employee_number, row['Nombre_de_EC'], row['Sucursal'], row['Categoria'])
                print(f'El dato con Legajo: {employee_number} fue cargado con exito')
            else:
                print(f"El employeeNumber {employee_number} ya existe y se omitirá.")
        else:
            print(f"Advertencia: Fila {index + 2} en el archivo CSV no coincide con la estructura esperada y se omitirá.")
    connection.commit()


def fetch_data_and_create_json(db_connection, json_file):  #  3ro
    connection = db_connection.connect()
    cursor = connection.cursor()    
    query = "SELECT employeeNumber, fullName, branch, category FROM dbo.tec_payrollVM"
    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        employee_number, full_name, branch, category = row
        data.append({
            "employeeNumber": employee_number,
            "fullName": full_name,
            "branch": branch,
            "category": category,
            "Observations": ""
        })
    result_dict = {"Nomina": data}
    with open(json_file, 'w') as file:
        json.dump(result_dict, file, indent=2)
        
        


# get_existing_employee_numbers(conexion)
insert_data_from_csv(csv_filename, conexion)
fetch_data_and_create_json(conexion, json_file)
