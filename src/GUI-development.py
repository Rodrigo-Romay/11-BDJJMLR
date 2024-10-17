import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import pandas as pd
import sqlite3

class GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Data Import App")
        self._file = None

        self.create_widgets()  # Crear widgets

    def create_widgets(self):

        load_button = tk.Button(self.root, text="Load File", command=self.load_file)  # Botón para seleccionar archivo
        load_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="File's Route:")  # Mostrar la ruta del archivo seleccionado
        self.file_label.pack(pady=10)

        self.table_frame = tk.Frame(self.root)  # Crear frame con scrollbar
        self.table_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.v_scroll = tk.Scrollbar(self.table_frame, orient="vertical")
        self.h_scroll = tk.Scrollbar(self.table_frame, orient="horizontal")

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        # Configurar el Treeview correctamente con los scrollbars
        self.data_table = ttk.Treeview(self.table_frame, 
                                       yscrollcommand=self.v_scroll.set, 
                                       xscrollcommand=self.h_scroll.set)
        self.data_table.pack(expand=True, fill="both")

        # Asignar la función de scroll a los widgets
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

            # Detectar tipo de archivo y cargar datos
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.csv':
                self.load_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                self.load_excel(file_path)
            elif file_extension in ['.db', '.sqlite']:
                self.load_sqlite(file_path)
            else:
                messagebox.showerror("Unsupported File", "The selected file type is not supported.")

    def load_csv(self, file_path):
        try:
            data = pd.read_csv(file_path)
            self.display_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the CSV file: {str(e)}")

    def load_excel(self, file_path):
        try:
            data = pd.read_excel(file_path)
            self.display_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the Excel file: {str(e)}")

    def load_sqlite(self, file_path):
        try:
            conn = sqlite3.connect(file_path)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)
            table_name = tables.iloc[0, 0]  # Asume que se toma la primera tabla en la base de datos
            data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            self.display_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the SQLite database: {str(e)}")

    def display_data(self, data):
        # Limpiar cualquier dato anterior en el Treeview
        self.data_table.delete(*self.data_table.get_children())

        # Crear columnas dinámicamente según el archivo cargado
        self.data_table["columns"] = list(data.columns)

        # Configurar encabezados
        for col in data.columns:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, width=150)  # Puedes ajustar el ancho según lo que necesites

        # Insertar filas de datos
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

