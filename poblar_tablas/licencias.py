import json
from db.conection import DatabaseConnection
import pandas as pd
import numpy as np
from datetime import datetime

conexion = DatabaseConnection()
csv_filename = 'datos_licencias.csv'


def insert_data_from_csv(csv_file, db_connection):
    df = pd.read_csv(csv_file)
    connection = db_connection.connect()
    cursor = connection.cursor()       
    for index, row in df.iterrows():
        employeeNumber = row['employeeNumber']
        fullName = row['fullName']
        descriptions = row['descriptions']
        startDay = datetime.strptime(row['startDay'], '%Y-%m-%d').strftime('%Y-%m-%d')
        endDay = datetime.strptime(row['endDay'], '%Y-%m-%d').strftime('%Y-%m-%d')
        filterDays = row['filterDays']
        licenseDays = row['licenseDays']
        insert_sql = "INSERT INTO tec_licenseReports (employeeNumber, fullName, descriptions, startDay, endDay, filterDays, licenseDays) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(insert_sql, employeeNumber, fullName, descriptions, startDay, endDay, filterDays, licenseDays)
        print(f'El dato con Legajo: {employeeNumber} fue cargado con éxito')       
    connection.commit()
    

insert_data_from_csv(csv_filename, conexion)

