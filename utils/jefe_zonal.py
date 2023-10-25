import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path_nomina = os.path.join(current_dir, 'data', 'json', 'nomina.json')


def handle_form_submission(jefe_zonal, nomina=json_path_nomina):
    with open(nomina, 'r') as file_nomina:
        data_metas = json.load(file_nomina)
        nomina = data_metas['Nomina']    
    filtered_nomina = [entry for entry in nomina if entry['jefe_a_cargo'] == jefe_zonal]
    return filtered_nomina