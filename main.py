# This is a sample Python script.
import logging
import tkinter as tk
import ttkbootstrap as tb
from gui.download_dof import DownloadDof
from gui.search_dof import SearchDof

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def show_download():
    # Clear current widgets from main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    # Load DownloadDof GUI
    download_frame = DownloadDof(main_frame)
    download_frame.pack(fill="both", expand=True)

def show_finder():
    # Clear current widgets from main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    # Load SerchDof GUI
    search_frame = SearchDof(main_frame)
    search_frame.pack(fill="both", expand=True, pady=20)

def main():
    logging.basicConfig(level=logging.INFO)

    root = tb.Window(themename="cosmo")
    root.title('Redof - Recuperar publicaciones del DOF Yucatán')
    root.iconbitmap("C:/Proyectos/Python/Redof/redof.ico")

    app_width = 900
    app_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')

    # Global main_frame setup
    global main_frame
    main_frame = tb.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Menu
    menu_principal = tk.Menu(root)
    file_menu = tk.Menu(menu_principal, tearoff=0)
    file_menu.add_command(label="Descargar", command=show_download)
    file_menu.add_command(label="Buscar", command=show_finder)
    file_menu.add_command(label="Salir", command=root.quit)
    menu_principal.add_cascade(label="Archivo", menu=file_menu)
    root.config(menu=menu_principal)
    footer_frame = tb.Frame(root)
    footer_frame.pack(side="bottom", fill="x")
    copyright_label = tb.Label(footer_frame, text="© 2025 @crowslayer - Versión 1.0",
                               font=("Arial", 9), foreground="gray")
    copyright_label.pack(pady=5)
    # Show download frame by default
    # show_download()
    show_finder()
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
