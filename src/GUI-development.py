import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from Modulo import DataImport as dti

class GUI():
       
    def __init__(self, root):

        self.root = root
        self.root.title("Data Import App")
        self._file = None

        self.create_widgets() # Crear widgets

    def create_widgets(self):

        load_button = tk.Button(self.root, text="Load File", command=self.load_file) # Botón para seleccionar archivo
        load_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="File's Route:") # Mostrar la ruta del archivo seleccionado
        self.file_label.pack(pady=10)

        self.table_frame = tk.Frame(self.root) # Crear frame con scrollbar
        self.table_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.v_scroll = tk.Scrollbar(self.table_frame, orient="vertical")
        self.h_scroll = tk.Scrollbar(self.table_frame, orient="horizontal")

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        self.data_table = ttk.Treeview(self.table_frame, yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.data_table.pack(expand=True, fill="both")

        self.v_scroll.config(command=self.data_table.yview)
        self.h_scroll.config(command=self.data_table.xview)

    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("SQLite Files", "*.db *.sqlite")]
        )
        
        if file_path:
            self._file = file_path
            self.file_label.config(text=f"File's Route: {self._file}")
            dti(self._file).file_type()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()