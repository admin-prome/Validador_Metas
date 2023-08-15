import json

def get_meta_q(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return meta['cantidad']
    return "0"

