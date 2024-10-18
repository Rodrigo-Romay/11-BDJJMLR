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

        # Hace que la ventana sea redimensionable
        self.root.geometry("800x600")  # Tamaño inicial
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        load_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="File's Route:")
        self.file_label.pack(pady=10)

        # Configurar el Frame con el Treeview y el Scrollbar
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(padx=5, pady=5, fill="both", expand=True)
        self.table_frame.pack_propagate(False)  # Evita que el frame cambie de tamaño

        self.v_scroll = tk.Scrollbar(self.table_frame, orient="vertical")
        self.h_scroll = tk.Scrollbar(self.table_frame, orient="horizontal")

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        self.data_table = ttk.Treeview(self.table_frame, yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.data_table.pack(expand=True, fill="both")

        self.v_scroll.config(command=self.data_table.yview)
        self.h_scroll.config(command=self.data_table.xview)

        # Ajusta el tamaño de las columnas dinámicamente al cambiar el tamaño de la ventana
        self.data_table.bind("<Configure>", self.center_columns_in_window)

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
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file: {str(e)}")

    def display_data(self, data):
        # Limpiar cualquier dato anterior en el Treeview
        self.data_table.delete(*self.data_table.get_children())

        # Crear columnas dinámicamente según el archivo cargado
        self.data_table["columns"] = list(data.columns)

        for col in data.columns:
            self.data_table.heading(col, text=col, anchor="center")  # Centrar los encabezados
            self.data_table.column(col, anchor="center")  # Centrar el contenido de las columnas

        # Insertar filas de datos
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))

        # Llama a ajustar el tamaño de las columnas según el tamaño de la ventana
        self.center_columns_in_window()

    def center_columns_in_window(self, event=None):
        # Obtener el ancho total disponible del Treeview
        tree_width = self.data_table.winfo_width()
        total_columns = len(self.data_table["columns"])
        
        if total_columns > 0:
            # Calcular el ancho necesario para todas las columnas combinadas
            total_data_width = total_columns * 150  # Ancho estimado por columna
            if total_data_width < tree_width:
                # Si el ancho total de las columnas es menor que el Treeview, calcular el margen
                remaining_space = tree_width - total_data_width
                padding = remaining_space // 2  # Dividir el espacio restante para centrar

                # Crear columnas vacías a los lados para centrado visual
                self.data_table["show"] = "headings"  # Asegurar que solo se muestren los encabezados
                self.data_table.column("#0", width=padding, stretch=False)
                
                for col in self.data_table["columns"]:
                    self.data_table.column(col, width=150, stretch=True)  # Asigna ancho a las columnas

            else:
                # Si las columnas ocupan más espacio que el Treeview, ajustarlas dinámicamente
                for col in self.data_table["columns"]:
                    self.data_table.column(col, width=max(tree_width // total_columns, 100), stretch=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()