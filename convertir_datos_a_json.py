import pandas as pd
import json
import numpy as np

def csv_to_json(csv_file, json_file):
    df = pd.read_csv(csv_file, delimiter='\t', na_filter=False)

    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.fillna("", inplace=True)

    # # Reemplazar las cadenas vacías en "Cant_Dias_Licencia" por 0
    # df["Cant_Dias_Licencia"].replace("", 0, inplace=True)

    data = df.to_dict(orient='records')

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)

csv_to_json('datos.csv', 'datos.json')
