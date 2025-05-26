import os
import requests
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class RequestDof:
    def __init__(self, logger = None):
        self.url_dof = 'https://www.yucatan.gob.mx/gobierno/diario_oficial.php?'
        self.domain_dof= 'https://www.yucatan.gob.mx'
        self.logger = logger or print
        self.path_destination = None
        self.progress_callback = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Encoding': 'gzip, deflate'
        })

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def range_dates(self, date_begin, date_end):
        try:
            current_date = datetime.now().date()
            begin_date = datetime.strptime(date_begin, '%Y-%m-%d').date()
            final_date = datetime.strptime(date_end, '%Y-%m-%d').date()

            if begin_date > current_date:
                raise  ValueError('La fecha de inicio no puede ser mayor a la fecha actual.')

            if final_date > current_date:
                raise  ValueError('La fecha final no puede ser mayor a la fecha actual.')

            if begin_date > final_date:
                raise ValueError('La fecha de inicio no puede ser mayor a la fecha final.')

            dates = []
            while begin_date <= final_date:
                if begin_date.weekday() < 5:
                    dates.append(begin_date)
                begin_date += timedelta(days=1)
            return  dates

        except ValueError as e:
            self.logger(f"El formato de fecha no es valido. {e}")
            return []

    def process_request(self, begin_date, end_date, destination_path, progress_callback=None):
        try:
            self.progress_callback = progress_callback
            self.path_destination = destination_path

            if not destination_path:
                raise ValueError ( 'No se proporciono la ruta destino')

            dates = self.range_dates(begin_date, end_date)
            if not dates:
                raise ValueError("No hay fechas válidas en el rango.")

            tasks = []
            total_files = 0
            with ThreadPoolExecutor(max_workers=6) as executor:

                for i, date in enumerate(dates, 1):
                    url = f"{self.url_dof}f={date.year}-{date.month}-{date.day}"
                    links = self.scrap_dof_page(url)
                    file_path = os.path.join(destination_path, str(date.year), f"{date.month:02d}")

                    for link in links:
                        tasks.append(executor.submit(self.download_with_progress, link, file_path))

                for future in as_completed(tasks):
                    try:
                        result =  future.result()

                        if result:
                            total_files += 1
                    except Exception as e:
                        self.logger(f"❌ Error en tarea: {e}")

            return total_files

        except Exception as e:
            self.logger(f'Ocurrió un error. {e}')
            return 0

    def scrap_dof_page(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
            links = []
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # scraping href dof
            for row in soup.select('div.seccion_pagina a'):
                h = row.get('href')
                if not h:
                    continue
                link = self.domain_dof + h
                links.append(link)

            return links

        except Exception as e:
            self.logger(f'Error al extraer contenido. {e}')
            return []

    def download_with_progress(self, url: str, path: str):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            filename = os.path.join(path, url.split("/")[-1])

            if os.path.exists(filename):
                self.logger(f"⚠️ Archivo ya existe, se omite: {filename}")
                return False

            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                if int(response.headers.get('content-length', 0)) == 0:
                    self.logger(f"⚠️ Archivo vacío: {url}")
                    return False

                with open(filename, 'wb') as file:
                    for data in response.iter_content(1024):
                        file.write(data)

                self.logger(f"Archivo descargado: {filename}")

                if filename.endswith(".zip"):
                    zip_folder_name = Path(filename).stem
                    extract_path = os.path.join(path, zip_folder_name)
                    os.makedirs(extract_path, exist_ok=True)

                    with zipfile.ZipFile(filename, 'r') as zip_ref:
                        zip_ref.extractall(path)
                        extracted_files = zip_ref.namelist()

                    self.logger(f"ZIP extraído en: {extract_path}")

                    for f in extracted_files:
                        self.logger(f"  └─ {f}")

                    # 🚫 Opcional: Eliminar el zip después de extraer
                    os.remove(filename)
                    self.logger(f"ZIP eliminado: {filename}")
                return True
            return False
        except requests.RequestException as e:
            self.logger(f'🌐 Error de red: {e}')
            return False
        except zipfile.BadZipFile as e:
            self.logger(f'❌ El archivo no es un ZIP válido: {e}')
            return False
        except Exception as e:
            self.logger(f'❗ Error inesperado al descargar: {e}')
            return False
        
    def write_log(self, message: str):
        try:
            log_path = os.path.join(self.path_destination or ".", "descargas.log")
            with open(log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            self.logger(f"No se pudo escribir en el log: {e}")
