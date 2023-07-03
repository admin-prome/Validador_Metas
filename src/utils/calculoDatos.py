import json



def read_ajustes():
    with open('data/json/ajustes.json') as file:
        data = json.load(file)
    return data
# print(read_ajustes())



def read_metas():
    with open('data/json/metas.json') as file:
        data = json.load(file)
    return data
# print(read_metas())




def read_progresiones():
    with open('data/json/progresiones.json') as file:
        data = json.load(file)
    return data
# print(read_progresiones())



def read_progresion_of_users():
    with open('data/json/progresionOfUsers.json') as file:
        data = json.load(file)
    return data
# print(read_progresion_of_users())



def read_tutores():
    with open('data/json/tutores.json') as file:
        data = json.load(file)
    return data
# print(read_tutores())



def read_users():
    with open('data/json/users.json') as file:
        data = json.load(file)
    return data
# print(read_users())


def users_mails():
    with open('data/json/users.json') as user_file:
        data = json.load(user_file)
    users = data['Users']
    emails = [user['mail'] for user in users]  # Obtener los correos electrónicos de cada usuario
    return emails
# print(users_mails())



def read_nomina():
    with open('data/json/nomina.json') as file:
        data = json.load(file)
    result = []
    for obj in data["Nomina"]:
        result.append(obj)
        legajo = obj["legajo"]
        print(legajo)
    return result

# read_nomina()


def read_tutores():
    with open('data/json/tutores.json') as file:
        data = json.load(file)
    result = []
    for obj in data['Tutores']:
        result.append(obj)
        legajo = obj['legajo']
        print(legajo)
    return result

# read_tutores()


def compare_legajos():
    nomina_data = read_nomina()
    tutores_data = read_tutores()
    tutores_legajos = [tutor['legajo'] for tutor in tutores_data]
    
    for legajo in tutores_legajos:
        if legajo in [obj['legajo'] for obj in nomina_data]:
            print(f"El legajo {legajo} existe tanto en la nómina como en los tutores.")
        else:
            print(f"El legajo {legajo} no existe en la nómina.")

compare_legajos()




def tutoria(legajo):
    with open('data/json/nomina.json') as nomina_file:
        nomina_data = json.load(nomina_file)['Nomina']
    with open('data/json/tutores.json') as tutores_file:
        tutores_data = json.load(tutores_file)['Tutores']        
    legajos_nomina = [user['legajo'] for user in nomina_data]
    legajos_tutores = [tutor['legajo'] for tutor in tutores_data]
    if legajo in legajos_nomina or legajo in legajos_tutores:
        return True
    else:
        return False











