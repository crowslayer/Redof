import os
import tkinter as tk
import csv
import pathlib
from pathlib import Path
from threading import Thread
from tkinter import ttk
from tkinter.filedialog import askdirectory, asksaveasfilename
from openpyxl import Workbook
from app.dof_searcher import DofSearcher

MENU_REVEAL = 0
MENU_EXPORT = 1

class SearchDof(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables
        self.search_path_var = tk.StringVar(value=str(pathlib.Path().absolute()))
        self.search_term_var = tk.StringVar(value='txt')
        self.search_type_var = tk.StringVar(value='endswidth')
        self.search_count = 0

        # container for user input
        input_labelframe = ttk.Labelframe(self, text='Completa el formulario para iniciar la busqueda', padding=(20, 10, 10, 5))
        input_labelframe.pack(side='top', fill='x')
        input_labelframe.columnconfigure(1, weight=1)

        # file path input
        ttk.Label(input_labelframe, text='Carpeta con DOFs').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(input_labelframe, textvariable=self.search_path_var)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='Browse', command=self.on_browse, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # search term input
        ttk.Label(input_labelframe, text='Texto').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        e2 = ttk.Entry(input_labelframe, textvariable=self.search_term_var)
        e2.grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        b2 = ttk.Button(input_labelframe, text='Buscar', command=self.on_search, style='primary.Outline.TButton')
        b2.grid(row=1, column=2, sticky='ew', pady=2)

        # search type selection
        ttk.Label(input_labelframe, text='Criterio').grid(row=2, column=0, padx=10, pady=2, sticky='ew')
        option_frame = ttk.Frame(input_labelframe, padding=(15, 10, 0, 10))
        option_frame.grid(row=2, column=1, columnspan=2, sticky='ew')
        r1 = ttk.Radiobutton(option_frame, text='Contiene', value='contains', variable=self.search_type_var)
        r1.pack(side='left', fill='x', pady=2, padx=10)
        r2 = ttk.Radiobutton(option_frame, text='Inicia con...', value='startswith', variable=self.search_type_var)
        r2.pack(side='left', fill='x', pady=2, padx=10)
        r3 = ttk.Radiobutton(option_frame, text='Termina con...', value='endswith', variable=self.search_type_var)
        r3.pack(side='left', fill='x', pady=2, padx=10)
        r1.invoke()
        r2.configure(state='disabled')
        r3.configure(state='disabled')

        # search results tree
        self.tree = ttk.Treeview(self, style='info.Treeview')
        self.tree.pack(fill='both', pady=5)
        self.tree['columns'] = ('date', 'num', 'page', 'paragraph', 'path')
        self.tree.column('#0', width=200)
        self.tree.heading('#0', text='Name')
        self.tree.heading('path', text='Path')

        self.tree.heading('page', text='Página')
        self.tree.heading('paragraph', text='Texto Publicación')
        self.tree.heading('num', text='Número')
        self.tree.heading('date', text='Fecha')

        self.tree.column('page', width=50, anchor='center')
        self.tree.column('paragraph', width=400, anchor='w')
        self.tree.column('num', width=100, anchor='center')
        self.tree.column('date', width=300, anchor='w')

        # progress bar
        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate',
                                           style='success.Horizontal.TProgressbar')
        self.progressbar.pack(fill='x', pady=5)

        # right-click menu for treeview
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label='Reveal in file manager', command=self.on_doubleclick_tree)
        self.menu.add_command(label='Export a results to csv', command=self.export_to_csv)

        # event binding
        self.tree.bind('<Double-1>', self.on_doubleclick_tree)
        self.tree.bind('<Button-3>', self.right_click_tree)

        # Añadir label de versión / copyright abajo


    def on_browse(self):
        """Callback for directory browse"""
        path = askdirectory(title='Directory',initialdir=Path.home())
        if path:
            self.search_path_var.set(path)

    def on_doubleclick_tree(self, event=None):
        try:
            selected_id = self.tree.selection()[0]
            values = self.tree.item(selected_id, 'values')

            if not values:
                return  # Es un nodo raíz ("Search 1"), no hacer nada

            pdf_path = values[-1]
            if os.path.exists(pdf_path):
                os.startfile(pdf_path)
            else:
                print(f"⚠️ Archivo no encontrado: {pdf_path}")

        except Exception as e:
            print(f"⚠️ Error al abrir PDF: {e}")

    def right_click_tree(self, event=None):
        try:
            id = self.tree.selection()[0]
        except IndexError:
            return
        if id.startswith('I'):
            self.menu.entryconfigure(MENU_EXPORT, state='disabled')  # Export results to csv
            self.menu.entryconfigure(MENU_REVEAL, state='normal')  # Reveal in file manager
        else:
            self.menu.entryconfigure(MENU_EXPORT, state='normal')
            self.menu.entryconfigure(MENU_REVEAL, state='disabled')
        self.menu.post(event.x_root, event.y_root)

    def on_search(self):
        """Search for a term based on the search type"""
        term = self.search_term_var.get()
        search_path = self.search_path_var.get()
        search_type = self.search_type_var.get()
        if not term:
            return

        self.progressbar.start(10)
        self.search_count += 1
        tree_id = self.tree.insert('', 'end', self.search_count, text=f'Search {self.search_count}')
        self.tree.item(tree_id, open=True)

        def run_search():
            searcher = DofSearcher(term, search_path, search_type)
            results = searcher.search()
            self.after(0, lambda: self.update_results(results, tree_id))

        Thread(target=run_search, daemon=True).start()

    def update_results(self, results, tree_id):
        self.progressbar.stop()
        for result in results:
            self.insert_row(result, tree_id)

    def reveal_in_explorer(self, id):
        values = self.tree.item(id, 'values')
        path = pathlib.Path(values[-1]).absolute().parent
        os.startfile(path)

    def export_to_csv(self, event=None):
        try:
            id = self.tree.selection()[0]
        except IndexError:
            return

        filename = asksaveasfilename(
            initialfile='results',
            filetypes=[('Excel Workbook', '*.xlsx'), ('CSV (Comma delimited)', '*.csv')],
            defaultextension=".xlsx"
        )
        if not filename:
            return

        # Get tree items
        children = self.tree.get_children(id)
        rows = [['Name', 'Fecha de Publicación', 'Número de Diario', 'Página', 'Extracto', 'Path']]
        for child in children:
            name = self.tree.item(child, 'text')
            values = self.tree.item(child, 'values')
            rows.append([name] + list(values))

        if filename.endswith('.csv'):
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        elif filename.endswith('.xlsx'):
            wb = Workbook()
            ws = wb.active
            for row in rows:
                ws.append(row)
            wb.save(filename)

        os.startfile(filename)

    def insert_row(self, match, parent_id):
        try:
            iid = self.tree.insert(parent_id, 'end', text=match['name'],
                                                          values=(match.get('date', ''), match.get('num', ''), match['page'], match['paragraph'] ,match['path'],
                                                                  ) )
            self.tree.selection_set(iid)
            self.tree.see(iid)
        except Exception as e:
            print(f"⚠️ Error insertando fila: {e}")