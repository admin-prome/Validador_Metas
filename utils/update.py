from db.conection import DatabaseConnection 

def employeeNumberToUpdate(legajo):
    conexion = DatabaseConnection()
    connection = conexion.connect()
    cursor = connection.cursor()
    select_query = "SELECT employeeNumber, fullName, Observations FROM dbo.tec_payrollVM WHERE employeeNumber = ?"
    cursor.execute(select_query, legajo)
    result = cursor.fetchone()
    if result:
        observacion_actual = result
    else:
        observacion_actual = ""
    return observacion_actual