import os
import traceback
import pyodbc
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path)
        self.sql_server = os.getenv("SQL_DB_HOST")
        self.sql_db = os.getenv("SQL_DB")
        self.sql_user = os.getenv("SQL_USER")
        self.sql_pass = os.getenv("SQL_PASSWORD")
             
    def connect(self):
        try:
            conexion = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.sql_server};DATABASE={self.sql_db};UID={self.sql_user};PWD={self.sql_pass}')
            print(f'Conexion exitosa a la Base de datos: {self.sql_server}')
            return conexion
        except Exception as e:
            print(f'Error al intentar conectarse a la base de "{self.sql_server}"')
            traceback.print_exc()
      
