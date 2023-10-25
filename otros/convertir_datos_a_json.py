import pandas as pd
import json
import numpy as np

def csv_to_json(csv_file, json_file):
    try:
        df = pd.read_csv(csv_file, delimiter='\t', na_filter=False)
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        df.fillna("", inplace=True)
        data = df.to_dict(orient='records')
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)
        print(f'\nArchivo JSON creado con exito\n')
    except Exception as er:
        print(er)

csv_to_json('otros/datos.csv', 'otros/datos.json')
