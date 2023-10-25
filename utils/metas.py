import json
import os
from datetime import datetime


def get_meta_q(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return int(meta['cantidad']/2)
    return ""


def get_meta_monto(categoria):
    with open('data/json/metas.json') as file_metas:
        data_metas = json.load(file_metas)
    metas_q = data_metas['Metas']
    for meta in metas_q:
        if meta['categoria'] == categoria:
            return int(meta['monto']/2)
    return ""

