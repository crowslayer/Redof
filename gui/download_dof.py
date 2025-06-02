import sys
import os.path
import socket
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path

import ttkbootstrap as tb
from tkinter import filedialog, messagebox, ttk

from app.request_dof import RequestDof
from gui.console_redirect import ConsoleRedirect


class DownloadDof(tb.Frame):
    def __init__(self, root, title = ''):
        super().__init__(root)
        self.sv_destination_path = None
        self.title = title or 'Descarga de DOF'
        self.root = root
        self.color = {
            'black': '#161a1d',
            'gray': '#98989A',
            'red': '#9b2247',
            'green': '#1e5b4f',
            'gold': '#a57f2c',
            'red2': '#611232',
            'green2': '#002f2a',
            'gold2': '#e6d194'
        }
        self.pack(fill='both',expand=True)
        self.build_form()
        self.show_console()
        self.redirect_stdout_stderr()

    def build_form(self):
        self.show_title()
        self.show_input_label()
        self.show_entry_data()

    def show_title(self):
        lbl_title = tb.Label(self, text=self.title)
        lbl_title.config(padding=10, foreground=self.color['gold2'], font=('Verdana', 16, 'bold'))
        lbl_title.grid(column=0, row=0,columnspan=4, pady=10)

    def show_input_label(self):
        lbl_begin_date = tb.Label(self, text='Fecha Inicial: ')
        lbl_begin_date.config(foreground=self.color['green2'], font=('Arial', 11))
        lbl_begin_date.grid(column=0, row=1, padx=10, pady=5, sticky='nsew')

        lbl_final_date = tb.Label(self, text='Fecha Final: ')
        lbl_final_date.config(foreground=self.color['green2'], font=('Arial', 11))
        lbl_final_date.grid(column=0, row=2, padx=10, pady=5, sticky='nsew')

        lbl_destination_path = tb.Label(self, text='Directorio de salida')
        lbl_destination_path.config(foreground=self.color['green2'], font=('Arial', 11))
        lbl_destination_path.grid(column=0, row=3, padx=10, pady=5, sticky='nsew')

    def show_entry_data(self):
        style = ttk.Style()
        style.configure(
            "SEntry.TEntry",
            padding=5,
        )
        today = datetime.today().date()

        # self.sv_begin_date = tk.StringVar()
        self.ent_begin_date = tb.DateEntry(self, bootstyle='info',dateformat="%Y-%m-%d" )
        self.ent_begin_date.grid(column=1, row=1, padx=10, pady=5, columnspan=1, sticky='nsw')

        self.ent_final_date = tb.DateEntry(self, bootstyle='warning', dateformat="%Y-%m-%d"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           )
        self.ent_final_date.grid(column=1, row=2, padx=10, pady=5, sticky='nsw')

        self.sv_destination_path = tk.StringVar()
        ent_path_destination = tb.Entry(self, textvariable=self.sv_destination_path)
        ent_path_destination.config(width=50, font=('ARIAL', 12), state='normal', style="SEntry.TEntry")
        ent_path_destination.grid(column=1, row=3, padx=10, pady=5, sticky='nsew')

        tb.Button(self, text="Browse", style="info" ,command=self.get_path_destination).grid(column=2, row=3, sticky="w")

        tb.Button(self, text="Download", style="success"  ,width=10, command=self.download_dof).grid(column=0, row=4, padx=10, pady=5, sticky='nse')
        tb.Button(self, text="Quit", width=10 ,command=self.destroy).grid(column=1, row=4, padx=10, pady=5, sticky='nsw')

    def show_console(self):
        self.console = tb.ScrolledText(self, wrap='word', height=15, width=80, state='disabled')
        self.console.config(font=('Helvetica', 8), background=self.color['black'], foreground=self.color['gold2'])
        self.console.grid(column=0, row=8, columnspan=4, padx=10, pady=10, sticky="nsew")

    def update_console(self, message):
        self.console.config(state='normal')
        self.console.insert(tk.END, str(message) + '\n')
        self.console.config(state='disabled')
        self.console.see(tk.END)

    def get_path_destination(self):
        source = filedialog.askdirectory(initialdir=Path.home(), title='Directorio destino')
        self.sv_destination_path.set(source)

    def redirect_stdout_stderr(self):
        sys.stdout = ConsoleRedirect(self.update_console)
        sys.stderr = ConsoleRedirect(self.update_console)

    def is_connected(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
            return True
        except Exception as e:
            self.update_console(f'Error de coneccion a la red.')
            return False

    def download_dof(self):
        try:
           begin_date = self.ent_begin_date.entry.get()
           final_date = self.ent_final_date.entry.get()
           destination_path = self.sv_destination_path.get()

           if not begin_date:
               raise ValueError('Fecha inicial no puede ser vacia')
           if not final_date:
               raise ValueError('Fecha final no puede ser vacia')
           if not destination_path:
               raise ValueError('El directorio destino no puede ser vacío')

           today = datetime.today().date()
           b_date = datetime.strptime(begin_date, "%Y-%m-%d").date()
           f_date = datetime.strptime(final_date, "%Y-%m-%d").date()

           if b_date > today:
               raise ValueError("La fecha inicial no puede ser mayor a hoy.")
           if f_date > today:
               raise ValueError("La fecha final no puede ser mayor a hoy.")
           if b_date > f_date:
               raise ValueError("La fecha inicial no puede ser mayor a la final.")

           if not self.is_connected():
               raise ValueError("No hay conexión a internet. Verifica tu red.")

           threading.Thread(
               target=self.threaded_download,
               args=(begin_date, final_date, destination_path),
               daemon=True).start()

        except ValueError as e:
            self.update_console(f"{e}")
            messagebox.showerror('Error', f'{e}')

    def threaded_download(self, begin_date, final_date, destination_path):
        self.update_console("Descargando archivos...")
        try:
            request_dof = RequestDof(self.update_console)
            total_files = request_dof.process_request(begin_date, final_date, destination_path)
            self.update_console(f'✅ Archivos descargados: {total_files}')
            messagebox.showinfo("Descarga completa", f"Se descargaron {total_files} archivos.")

        except Exception as e:
            self.update_console(f"Error durante la descarga: {e}")
