import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from Modulo import DataImport

class GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Trendify")
        self._file = None

        # === Diseño ===
        ctk.set_appearance_mode("dark")  # Tema oscuro
        ctk.set_default_color_theme("blue")  # Tema con acentos azul apagado

        # Dimensiones iniciales y configuraciones de la ventana
        self.root.geometry("1000x700")  # Ventana grande y espaciosa
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # === Barra de título superior ===
        title_label = ctk.CTkLabel(self.root, 
                            text="Trendify", 
                            font=("Pacifico", 50, "bold"), 
                            text_color="#d1d9e6")
                            
        title_label.pack(pady=20) 

        # === Botón para cargar archivo ===
        load_button = ctk.CTkButton(self.root, text="Load File", command=self.load_file,
                                    corner_radius=15, width=170, height=50,
                                    fg_color="#5A6F7D", hover_color="#3C4F5A",
                                    text_color="white", font=("Roboto", 16, "bold"),
                                    border_color="#707070", border_width=1)
        load_button.pack(pady=15)

        # === Etiqueta para mostrar la ruta del archivo ===
        self.file_label = ctk.CTkLabel(self.root, text="File's Route:",
                                        font=("Roboto", 16), text_color="#A0A0A0")
        self.file_label.pack(pady=10)

        # === Crear un Frame externo con bordes redondeados y color suave ===
        outer_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#2B2B2B")
        outer_frame.pack(padx=40, pady=30, fill="both", expand=True)

        # === Frame interior donde irá el Treeview y Scrollbars ===
        self.table_frame = ctk.CTkFrame(outer_frame, corner_radius=15, fg_color="#383838")
        self.table_frame.pack(padx=15, pady=15, fill="both", expand=True)

        # === Scrollbars personalizadas ===
        self.v_scroll = ctk.CTkScrollbar(self.table_frame, orientation="vertical",
                                        fg_color="#555555", button_color="#777777")
        self.h_scroll = ctk.CTkScrollbar(self.table_frame, orientation="horizontal",
                                        fg_color="#555555", button_color="#777777")

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")


        self.data_table = ttk.Treeview(self.table_frame, yscrollcommand=self.v_scroll.set, 
                                        xscrollcommand=self.h_scroll.set, show="headings")
        self.data_table.pack(expand=True, fill="both")

        self.v_scroll.configure(command=self.data_table.yview)
        self.h_scroll.configure(command=self.data_table.xview)

        # === Cambios para hacer que la tabla se vea mejor ===
        style = ttk.Style()

        # Cambiar el estilo de las celdas
        style.configure("Treeview", font=("Roboto", 15), 
                        background="#2E2E2E", foreground="#A7FFA7",
                        fieldbackground="#2E2E2E", rowheight=28)

        # Cambiar el estilo de los encabezados
        style.configure("Treeview.Heading", font=("Roboto", 16, "bold"),
                        background="#4F4F4F", foreground="#464646", relief="raised")

        # Mapa de colores al seleccionar una fila
        style.map("Treeview", 
                    background=[("selected", "#4A4A4A")],  
                    foreground=[("selected", "#F0F0F0")], 
                    highlightcolor=[("selected", "#6B6B6B")],  
                    highlightthickness=[("selected", 1)])

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
    root = ctk.CTk()  # Usamos la ventana de customtkinter
    app = GUI(root)
    root.mainloop()

