import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from Modulo import DataImport

class GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Data Frame Interface")
        self._file = None

        self.create_widgets()  # Crear widgets

    def create_widgets(self):
        load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        load_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="File's Route:")
        self.file_label.pack(pady=10)

        self.table_frame = tk.Frame(self.root)
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

            try:
                data_importer = DataImport(self._file)
                data_importer.file_type()  # Detecta el tipo de archivo y carga los datos
                data = data_importer._data  # Obtener los datos cargados

                if data is not None:
                    self.display_data(data)
                else:
                    messagebox.showerror("Error", "No data to display. Please check the file.")
            
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except ValueError:
                messagebox.showerror("Error", "File format not valid or invalid data.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file: {str(e)}")

    def display_data(self, data):
        # Limpiar cualquier dato anterior en el Treeview
        self.data_table.delete(*self.data_table.get_children())

        # Crear columnas dinámicamente según el archivo cargado
        self.data_table["columns"] = list(data.columns)

        for col in data.columns:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, width=150)

        # Insertar filas de datos
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()


