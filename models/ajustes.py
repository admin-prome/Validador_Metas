from flask import Flask, redirect, render_template, request, send_file, session, url_for, jsonify
from utils.add_nomina import *
from utils.update_nomina import *

class Settings():
    def update_datos(self, conexion):
        print('Actualizando Datos sin ajuste')
        actualizar_datos(conexion)
        connection = conexion.connect()
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
        print('Actualizando ajuste')
        for legajo in legajos:
            ajustes_metas(conexion, legajo[0])
        cursor.close()
        connection.close()
        return redirect(url_for('nomina'))