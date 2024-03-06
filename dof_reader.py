import fitz
import re
import pandas
import os


def walk_path(path):
    files = []
    if not os.path.exists(path):
        return files

    for root, dirs, filenames in os.walk(path):
        for name in filenames:
            if os.path.isfile(os.path.join(root, name)) and name.endswith('pdf'):
                file_name = os.path.join(root, name)
                files.append(file_name)
    return files


def reader_dof(file_name: str, criteria: str = ''):
    num_exp = criteria
    if len(num_exp) == 0:
        return False

    with fitz.open(file_name) as doc:
        text = ""
        first_page = doc.load_page(0).get_text()
        first_page = first_page.replace('�', '')
        paneling = first_page.split("\n")
        date_dof = paneling[0]
        num_dof = paneling[2]
        for page in doc:
            text += page.get_text()
    text = text.replace('�', '')
    lines = text.split("\n")
    # pattern = re.compile(r'(.*)(\b\w{1,5}/\w{1,4})')
    pattern = re.compile(fr"(.*)(\b.+{num_exp})")

    result = []
    for line in lines:
        exp = pattern.findall(line)
        if len(exp) == 0:
            continue
        for item in exp:
            result.append([date_dof, num_dof, item[0], item[1]])
    if len(result) == 0:
        return False

    print("Se encontraron %s coincidencias en DOF %s  de fecha %s" % (len(result), num_dof, date_dof))
    return result


def reader_dofs(path: str, criteria: str = ''):
    if len(path) == 0:
        print('Debe proporcionar la ruta donde se encuentras los archivos')
        exit(403)
    if len(criteria) == 0:
        print('Debe proporcionar el numero de expediente a localizar')
        exit(403)

    files = walk_path(path)

    if len(files) == 0:
        print('No se encontraron archivos en la ruta proporcionada')
        return False
    # leyendo archivo
    result = []
    for file in files:
        finded = reader_dof(file, criteria)
        if not finded or len(finded) == 0:
            continue

        result.extend(finded)
    return result


# Programa principal para lectura
files_path = input("Introduce la ruta donde se encuentran los DOF ")
record = input('Introduce el numero de expediente a buscar: 314/2024 ')
path_result = input('Introduce la ruta de destino en caso de haber coincidencias: ')
filename = input('Introduce el nombre del archivo donde se almacenaran las coincidencias: ')

content = reader_dofs(files_path, record)

if len(path_result) == 0:
    path_result = files_path + '/finding/'

if len(filename) == 0:
    filename = 'resultado'

if len(content) == 0:
    print('No se encontraron resultados')
    exit(200)
else:
    if not os.path.exists(path_result):
        os.makedirs(path_result)

    filename_result = '{0}{1}.xlsx'.format(path_result, filename)

    pd = pandas.DataFrame(content, columns=['Fecha DOF', 'Num. DOF', 'Fragmento', 'Expediente'])
    pd.to_excel(fr"{filename_result}")
    print('-----------------------------------------------\n')
    print('Consulta el archivo {} para revisar los detalles'.format(filename_result))

exit(200)
