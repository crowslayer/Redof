import logging
import tkinter as tk
import ttkbootstrap as tb
import os
import sys
from typing import Optional
from gui.download_dof import DownloadDof
from gui.search_dof import SearchDof

def resource_path(relative_path: str) -> str:
    base_path: Optional[str]
    if hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RedofApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Redof - Recuperar publicaciones del DOF Yucatán')

        # Cargar icono con manejo de errores
        try:
            icon_path = resource_path("redof.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            logging.warning(f"No se pudo cargar el icono: {e}")

        # Frame principal
        self.main_frame = tb.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Menú
        self.setup_menu()

        # Footer
        self.setup_footer()

        # Mostrar búsqueda por defecto
        self.show_finder()

    def setup_menu(self):
        menu_principal = tk.Menu(self.root)
        archivo_menu = tk.Menu(menu_principal, tearoff=0)
        archivo_menu.add_command(label="Descargar", command=self.show_download)
        archivo_menu.add_command(label="Buscar", command=self.show_finder)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        menu_principal.add_cascade(label="Archivo", menu=archivo_menu)
        self.root.config(menu=menu_principal)

    def setup_footer(self):
        footer_frame = tb.Frame(self.root)
        footer_frame.pack(side="bottom", fill="x")
        copyright_label = tb.Label(
            footer_frame,
            text="© 2025 @crowslayer - Versión 1.0",
            font=("Arial", 9),
            foreground="gray"
        )
        copyright_label.pack(pady=5)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_download(self):
        self.clear_main_frame()
        download_frame = DownloadDof(self.main_frame)
        download_frame.pack(fill="both", expand=True)

    def show_finder(self):
        self.clear_main_frame()
        search_frame = SearchDof(self.main_frame)
        search_frame.pack(fill="both", expand=True, pady=20)

def main():
    logging.basicConfig(level=logging.INFO)
    app_width, app_height = 900, 600
    root = tb.Window(themename="cosmo", size=(app_width, app_height))
    # Centrar la ventana
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    app = RedofApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
