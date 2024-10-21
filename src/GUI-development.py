import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from Modulo import DataImport

class GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Data Frame Interface")
        self._file = None

        # Configurar tema oscuro y azul predeterminado
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Dimensiones iniciales y configuraciones
        self.root.geometry("900x650")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Botón para cargar archivo con estilo personalizado
        load_button = ctk.CTkButton(self.root, text="Load File", command=self.load_file, 
                                    corner_radius=10, width=150, height=40,
                                    fg_color="#3b5998", hover_color="#2e4370",
                                    text_color="white", font=("Arial", 14, "bold"))
        load_button.pack(pady=20)

        # Etiqueta para mostrar la ruta del archivo con fuente más gruesa y texto blanco más brillante
        self.file_label = ctk.CTkLabel(self.root, text="File's Route:", 
                                       font=("Arial", 14, "bold"), text_color="white") 
        self.file_label.pack(pady=10)

        # Crear un Frame externo con bordes redondeados simulados
        outer_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#2f2f2f")
        outer_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Configurar el Frame interior donde irá el Treeview y Scrollbars
        self.table_frame = ctk.CTkFrame(outer_frame, corner_radius=15, fg_color="#2f2f2f")
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbars personalizadas
        self.v_scroll = ctk.CTkScrollbar(self.table_frame, orientation="vertical")
        self.h_scroll = ctk.CTkScrollbar(self.table_frame, orientation="horizontal")

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        # Usa ttk.Treeview para la tabla de datos
        self.data_table = ttk.Treeview(self.table_frame, yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.data_table.pack(expand=True, fill="both")

        self.v_scroll.configure(command=self.data_table.yview)
        self.h_scroll.configure(command=self.data_table.xview)

        # Ajusta el tamaño de las columnas dinámicamente al cambiar el tamaño de la ventana
        self.data_table.bind("<Configure>", self.center_columns_in_window)

        # Estilo del Treeview usando ttk.Style
        style = ttk.Style()
        style.configure("Treeview", 
                        font=("Arial", 18),  # Aumenta el tamaño de la fuente de los datos
                        background="#353535", 
                        foreground="white", 
                        fieldbackground="#1c1c1c", 
                        rowheight=35)

        # Cambia el tamaño de la fuente para los encabezados
        style.configure("Treeview.Heading", 
                        font=("Arial", 16, "bold"),  # Ajusta el tamaño de la fuente de los encabezados
                        background="black", 
                        foreground="black",
                        rowheight=45)

        style.map("Treeview", background=[("selected", "#3b5998")], foreground=[("selected", "white")])

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("SQLite Files", "*.db *.sqlite")]
        )

        if file_path:
            self._file = file_path
            self.file_label.configure(text=f"File's Route: {self._file}")

            try:
                data_importer = DataImport(self._file)
                data_importer.file_type()  # Detecta el tipo de archivo y carga los datos
                data = data_importer._data  # Obtener los datos cargados

                if not data.empty:
                    self.display_data(data)
                else:
                    messagebox.showerror("Error", "No data to display. Please check the file.")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except ValueError:
                messagebox.showerror("Error", "Invalid data.")
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

        # Ajusta el tamaño de las columnas según el tamaño de la ventana
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
    root = ctk.CTk() 
    app = GUI(root)
    root.mainloop()
