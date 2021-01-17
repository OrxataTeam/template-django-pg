import string
import random
import fileinput
import shutil
import os

def generate_secrect_key():
    lenght = 50
    # Get ascii Characters numbers and punctuation (minus quote characters as 
    # they could terminate string).
    chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')
    secret = ''.join([random.SystemRandom().choice(chars) for i in range(lenght)])
    return secret

print('Datos para la configuración de la plantilla Django-Postgres ')
app = input('aplication name: ')
user_and_group_app = input('introduce el usuario con el que se ejecutará la palicacion en Docker: ')
db_name = input('DataBase name: ')
db_user = input('Database user: ')
db_pass = input('Database password: ')
# db_host = input('Database host: ')

secret_key = generate_secrect_key()

# Reemplazamos el los ficheros de confuguracion el nombre de la app
replacements = {
        'django_template_app': '' + app + '',
        'my_secret_key': secret_key,
        'db_name_template': '' + db_name + '',
        'db_user_template': '' + db_user + '',
        'db_pass_template': '' + db_pass + '',
        'user_template_app': user_and_group_app,
        }
files = [
        'manage.py',
        'Dockerfile',
        'docker-compose.yml',
        'django_template_app/asgi.py',
        'django_template_app/settings.py',
        'django_template_app/wsgi.py',
        'django_template_app/urls.py'
        ]

for file in files:
    for line in fileinput.input(file, inplace=True):
        for search_for in replacements:
            replace_with = replacements[search_for]
            line = line.replace(search_for,replace_with)
        print(line, end='')

# #Reemplaamos el usuario y grupo en el que se ejecutara la aplicación en docker
# for line in fileinput.input('Dockerfile', inplace=True):
#     # print(line)
#     line = line.replace('user_template_app', user_and_group_app)
#     print(line, end='')

# # Reemplazamos datos db_user, db pass, db_name 
# replacements_db = {
#     'db_name_template': '' + db_name + '',
#     'db_user_template': '' + db_user + '',
#     'db_pass_template': '' + db_pass + '',
#     }
# for line in fileinput.input('docker-template.yml', inplace=True):
#     for search_for in replacements_db:
#         replace_with = replacements[search_for]
#         line = line.replace(search_for,replace_with)
#     print(line, end='')

# # Reemplazamos la Secret_key
# for line in fileinput.input('django_template_app/settings', inplace=True):
#     # print(line)
#     line = line.replace('user_template_app', user_and_group_app)
#     print(line, end='')
# my_secret_key

# cambio del nombre del directorio de la app
shutil.move('django_template_app', app)
os.remove('install-template.py')