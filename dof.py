import os.path
import zipfile
import requests
from datetime import datetime, timedelta
from tqdm.auto import tqdm as tq
from bs4 import BeautifulSoup


def download_data(url: str, path: str = "data/", verbose: bool = False):
    if not os.path.exists(path):
        os.makedirs(path)
    local_filename = os.path.join(path, url.split("/")[-1])
    r = requests.get(url, stream=True, verify=True)
    if r.status_code == 200:
        file_size = int(r.headers["Content-Length"]) if "Content-Length" in r.headers else 0
        chunk_size = 1024
        num_bars = int(file_size / chunk_size)
        if verbose:
            print(dict(file_size=file_size))
            print(dict(num_bars=num_bars))

        if not os.path.exists(local_filename):
            with open(local_filename, "wb") as fp:
                for chunk in tq(r.iter_content(chunk_size=chunk_size), total=num_bars, unit="B", desc=local_filename,
                                miniters=1, leave=True, unit_scale=True, unit_divisor=1024):
                    fp.write(chunk)  # type: ignore

        if ".zip" in local_filename:
            if os.path.exists(local_filename):
                with zipfile.ZipFile(local_filename, "r") as zip_ref:
                    zip_ref.extractall(path)
        return True


def download_with_progress(url: str, path: str = 'data/DOF/'):
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, url.split("/")[-1])

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with tq(desc=filename, unit="B", total=total_size, miniters=1, leave=True, unit_scale=True, unit_divisor=1024) as pbar:
            with open(filename, 'wb') as file:
                for data in response.iter_content(1024):
                    file.write(data)
                    pbar.update(len(data))
        return True


def list_dates(date_begin, date_end):
    inicio = datetime.strptime(date_begin, '%Y-%m-%d')
    fin = datetime.strptime(date_end, '%Y-%m-%d')
    date_list = [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") for d in range((fin - inicio).days + 1)]
    return date_list


def get_dof(date_begin, date_end, path_files='/DOF'):
    cont = 0
    date_list = list_dates(date_begin, date_end)
    extension_dof = 'pdf'
    base_url_dof = 'https://www.yucatan.gob.mx/docs/diario_oficial/diarios'
    # recorriendo fechas.
    for item in date_list:
        date = datetime.strptime(item, '%Y-%m-%d')
        year = date.year
        month = date.month
        filename = '%s_1.%s' % (item, extension_dof)
        url_dof = '%s/%s/%s' % (base_url_dof, year, filename)

        if len(path_files) == 0:
            destination_path = '%s/%s/%s' % (path_files, year, month)
        else:
            destination_path = '%s/DOF/%s/%s' % (path_files, year, month)

        result = download_data(url_dof, destination_path)
        if result:
            cont = cont + 1

    return cont


def download_dofs(links, path):
    if len(links) == 0:
        return False
    cont = 0
    for item in links:
        s = download_with_progress(item, path)
        if s:
            cont = cont + 1
    return cont


def get_scrap_dof(url):
    domain = 'https://www.yucatan.gob.mx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    links = []

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # scraping href dof
    for row in soup.select('div.seccion_pagina a'):
        h = row.get('href')
        if len(h) == 0:
            break
        link = domain + h

        links.append(link)

    return links


def get_dof_all(date_begin, date_end, path_files='/DOF'):

    link_dof = 'https://www.yucatan.gob.mx/gobierno/diario_oficial.php?'

    date_list = list_dates(date_begin, date_end)
    total = 0
    cont = 0
    for item in date_list:
        d = datetime.strptime(item, '%Y-%m-%d')
        f = 'f=%s-%s-%s' % (d.year, d.month, d.day)
        url = link_dof + f
        links = get_scrap_dof(url)

        if len(links) == 0:
            continue
        cont = download_dofs(links, path_files)
        total = total + cont
    return total


start_date = input("Introduce la fecha de inicio de la descarga en formato 'YYYY-MM-DD' : ")
end_date = input("Introduce la fecha de termino de la descarga en formato 'YYYY-MM-DD' : ")
files_path = input("Introduce la ruta de destino: ")
# descarga sin hacer scrap solo matutina
files = get_dof(start_date, end_date, files_path)
# Descarga haciendo scrap a la pagina y recuperanto toda la informacion.
#files = get_dof_all(start_date, end_date, files_path)

print('Se descargaron %d archivos de diario oficial' % (files))

exit(100)
