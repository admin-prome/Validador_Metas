import os
import shutil
import json
from datetime import datetime

def backUpJsonUsers():
    json_file = 'data/json/users.json'
    backup_dir = 'data/json/backup/backup_users'
    backup_file = f"users_backup_{datetime.now().strftime('%Y%m%d')}.json"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_path = os.path.join(backup_dir, backup_file)

    shutil.copy(json_file, backup_path)

    print(f"Archivo JSON respaldado en: {backup_path}")

# backUpJsonUsers()

def backUpJsonMetas():
    json_file = 'data/json/metas.json'
    backup_dir = 'data/json/backup/backup_metas'
    backup_file = f"metas_backup_{datetime.now().strftime('%Y%m%d')}.json"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_path = os.path.join(backup_dir, backup_file)

    shutil.copy(json_file, backup_path)

    print(f"Archivo JSON de metas respaldado en: {backup_path}")

# backUpJsonMetas()


def backUpJsonProgresiones():
    json_file = 'data/json/progresiones.json'
    backup_dir = 'data/json/backup/backup_progresiones'
    backup_file = f"progresiones_backup_{datetime.now().strftime('%Y%m%d')}.json"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_path = os.path.join(backup_dir, backup_file)

    shutil.copy(json_file, backup_path)

    print(f"Archivo JSON de progresiones respaldado en: {backup_path}")

# backUpJsonProgresiones()




