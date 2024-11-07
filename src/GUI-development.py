import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, IntVar, simpledialog
from tkinter import ttk
from Modulo import DataImport
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import pickle
import joblib
class GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Trendify")
        self._file = None
        self.columns_selected = []
        self.output_column = None 
        self._option_selected = False
        self.description = None

        # === Diseño ===
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        

        # Dimensiones iniciales y configuraciones de la ventana
        self.root.geometry("1000x700")
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
        load_button.pack(padx=10, pady=10)
        
        # === Botón para guardar el modelo ===
        save_button = ctk.CTkButton(self.root, text="Save Model", command=self.save_model, corner_radius=15, width=170, height=50,
                                    fg_color="#5A6F7D", hover_color="#3C4F5A", text_color="white", font=("Roboto", 16, "bold"),
                                    border_color="#707070", border_width=1)
        save_button.place(x=300, y=150)

        # === Etiqueta para mostrar la ruta del archivo ===
        self.file_label = ctk.CTkLabel(self.root, text="File's Route:",
                                        font=("Roboto", 16), text_color="#A0A0A0")
        self.file_label.pack(pady=10)

        # === Frame externo ===
        outer_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#2B2B2B")
        outer_frame.pack(padx=40, pady=10, fill="both", expand=True)

        # === Frame interior donde van el Treeview y Scrollbars ===
        self.table_frame = ctk.CTkFrame(outer_frame, corner_radius=15, fg_color="#383838")
        self.table_frame.pack(padx=15, pady=15, fill="both", expand=True)

        # === Scrollbars ===
        self.v_scroll = ctk.CTkScrollbar(self.table_frame, orientation="vertical",
                                        fg_color="#555555", button_color="#777777")
        self.h_scroll = ctk.CTkScrollbar(self.table_frame, orientation="horizontal",
                                        fg_color="#555555", button_color="#777777")

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        self.data_table = ttk.Treeview(self.table_frame, yscrollcommand=self.v_scroll.set, 
                                        xscrollcommand=self.h_scroll.set, show="headings")
        self.data_table.pack(expand=True, fill="both")

        # === Variable para manejar las opciones de nulos ===
        self.null_handling_option = ctk.StringVar(value="Select an option")

        # === Menú desplegable para manejar valores nulos ===
        self.null_option_menu = ctk.CTkOptionMenu(
            self.root,
            variable=self.null_handling_option,
            values=["Delete rows with nulls", "Fill with mean", "Fill with median", "Fill with constant"],
            command=self.handle_null_option,
            button_color="grey",
            text_color="white",
            fg_color="#383838",
            corner_radius=0
        )
        self.null_option_menu.place(x=35, y=170)
        self.null_option_menu.configure(state="disabled")
        self.null_option_menu.place_forget()

        # === Entrada para valor constante (inicialmente desactivada) ===
        self.constant_entry = ctk.CTkEntry(self.root, placeholder_text="Constant",
                                           width=80, height=30, font=("Roboto", 16), corner_radius=0, border_width=0)
        self.constant_entry.place(x=60, y=203)
        self.constant_entry.configure(state="disabled")
        self.constant_entry.place_forget()

        # === Botón para preprocesar datos ===
        self.preprocess_button = ctk.CTkButton(self.root, text="Preprocess Data", command=self.preprocess_data,
                                                corner_radius=15, width=170, height=100,
                                                fg_color="#5A6F7D", hover_color="#3C4F5A",
                                                text_color="white", font=("Roboto", 16, "bold"),
                                                border_color="#707070", border_width=1, anchor="n")
        self.preprocess_button.place(x=20, y=140)
        self.preprocess_button.configure(state="disabled")
        self.preprocess_button.lower()

        self.constant_entry.bind("<Return>", self.apply_constant_fill)
        self.root.bind("<Escape>", self.hide_constant_entry)

        # === Frame para las etiquetas de columnas ===
        self.labels_frame = ctk.CTkFrame(self.root)
        self.labels_frame.pack(pady=5, fill="x")

        # === Etiqueta para mostrar columnas de entrada seleccionadas ===
        self.input_columns_label = ctk.CTkLabel(self.labels_frame, text="Input Columns: None",
                                                font=("Roboto", 16), text_color="#A0A0A0")
        self.input_columns_label.pack(side="top", padx=(10, 0))

        # === Etiqueta para mostrar la columna de salida seleccionada ===
        self.output_column_label = ctk.CTkLabel(self.labels_frame, text="Output Column: None",
                                                font=("Roboto", 16), text_color="#A0A0A0")
        self.output_column_label.pack(side="bottom", padx=(10, 0))

        self.v_scroll.configure(command=self.data_table.yview)
        self.h_scroll.configure(command=self.data_table.xview)

        # === Cambios para hacer que la tabla se vea mejor ===
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 15), 
                        background="#2E2E2E", foreground="white",
                        fieldbackground="#2E2E2E", rowheight=28)

        style.configure("Treeview.Heading", font=("Roboto", 16, "bold"),
                        background="#4F4F4F", foreground="#464646", relief="raised")
        
        style.map("Treeview", 
                    background=[("selected", "#4A4A4A")],  
                    foreground=[("selected", "#F0F0F0")], 
                    highlightcolor=[("selected", "#6B6B6B")],  
                    highlightthickness=[("selected", 1)])

        # == Botones columnas ==
        self.select_columns_button = ctk.CTkButton(self.root, text="Select Input Columns ", command=self.select_columns,
                                                    corner_radius=15, width=170, height=50,
                                                    fg_color="#5A6F7D", hover_color="#3C4F5A",
                                                    text_color="white", font=("Roboto", 16, "bold"),
                                                    border_color="#707070", border_width=1)
        self.select_columns_button.place(x=20, y=20)
        self.select_columns_button.configure(state="disabled") 
        self.select_output_button = ctk.CTkButton(self.root, text="Select Output Column", command=self.select_output_column,
                                    corner_radius=15, width=170, height=50,
                                    fg_color="#5A6F7D", hover_color="#3C4F5A",
                                    text_color="white", font=("Roboto", 16, "bold"),
                                    border_color="#707070", border_width=1)
        self.select_output_button.place(x=20, y=80)
        self.select_output_button.configure(state="disabled")

        label = ctk.CTkLabel(root, text="Model description (Optional):")
        label.pack(pady=10)

        self.description_text = ttk.Entry(root,  width=40)
        self.description_text.pack(pady=10)

        create_button = ctk.CTkButton(root, text="Save description", command=self.model_description)
        create_button.pack(pady=20)
        

        self.create_model_button = ctk.CTkButton(self.root, text="Create Model", command=self.create_model,
                                                corner_radius=15, width=170, height=50,
                                                fg_color="#5A6F7D", hover_color="#3C4F5A",
                                                text_color="white", font=("Roboto", 16, "bold"),
                                                border_color="#707070", border_width=1)
        self.create_model_button.place(x=300, y=80)
        self.create_model_button.configure(state="disabled")

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
                    self.data_table_df= data
                    self.display_data(data)
                    self.preprocess_button.configure(state="normal") 
                    self.select_columns_button.configure(state="disabled")
                    self.select_output_button.configure(state="disabled")
                    self.null_option_menu.place_forget()
                    # Reiniciar las selecciones anteriores
                    self.columns_selected = []
                    self.output_column = None
                    self.input_columns_label.configure(text="Input Columns: None")
                    self.output_column_label.configure(text="Output Column: None")
                else:
                    self.data_table.delete(*self.data_table.get_children())
                    self.data_table["columns"]=list()
                    self.null_option_menu.place_forget()
                    self.select_columns_button.configure(state="disabled")
                    self.select_output_button.configure(state="disabled")
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
        # Crear columnas según el archivo cargado
        self.data_table["columns"] = list(data.columns)
        for col in data.columns:
            self.data_table.heading(col, text=col, anchor="center")
            self.data_table.column(col, anchor="center")
        # Insertar filas de datos
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))
        # Ajusta el tamaño de las columnas según el tamaño de la ventana
        self.center_columns_in_window()

    def center_columns_in_window(self, event=None):
        tree_width = self.data_table.winfo_width()
        total_columns = len(self.data_table["columns"])
        if total_columns > 0:
            total_data_width = total_columns * 150  # Ancho estimado por columna
            if total_data_width < tree_width:
                remaining_space = tree_width - total_data_width
                padding = remaining_space // 2  # Dividir el espacio restante para centrar
                self.data_table["show"] = "headings"  # Asegurar que solo se muestren los encabezados
                self.data_table.column("#0", width=padding, stretch=False)
                for col in self.data_table["columns"]:
                    self.data_table.column(col, width=150, stretch=True)
            else:
                for col in self.data_table["columns"]:
                    self.data_table.column(col, width=max(tree_width // total_columns, 100), stretch=True)

    def preprocess_data(self):
        if self.data_table_df is not None:
            # Contar valores nulos en cada columna
            null_counts = self.data_table_df.isnull().sum()
            self.null_counts_dict = null_counts[null_counts > 0].to_dict()
            if self.null_counts_dict:
                null_columns_info = '\n'.join([f"{col}: {count}" for col, count in self.null_counts_dict.items()])
                messagebox.showinfo("Null Values Detected", f"Null values found:\n{null_columns_info}")
                self.null_option_menu.configure(state="normal")
                self.null_option_menu.place(x=35, y=170)
            else:
                messagebox.showinfo("No Null Values", "No null values detected in the dataset.")
            self.preprocess_button.configure(state="disabled")
        else:
            messagebox.showwarning("No Data Loaded", "Please load data first.")

    def handle_null_option(self, option):
        if option == "Delete rows with nulls":
            confirm = messagebox.askyesno("Caution", "Are you sure to proceed?")
            if confirm:
                self.data_table_df.dropna(inplace=True)
                messagebox.showinfo("Rows Deleted", "Rows with null values have been deleted.")
                self.display_data(self.data_table_df)
                self.null_option_menu.configure(state="disabled")
                self.select_columns_button.configure(state="normal")
                self.select_output_button.configure(state="normal")

        elif option == "Fill with mean":
            confirm = messagebox.askyesno("Caution", "Are you sure to proceed?")
            if confirm:
                for col in self.null_counts_dict.keys():
                    if self.data_table_df[col].dtype in ['float64', 'int64']:
                        mean_value = round(self.data_table_df[col].mean(), 4)
                        self.data_table_df[col] = self.data_table_df[col].fillna(mean_value)
                messagebox.showinfo("Filled with Mean", "Null values have been filled with the mean of their respective columns.")
                self.display_data(self.data_table_df)
                self.null_option_menu.configure(state="disabled")
                self.select_columns_button.configure(state="normal")
                self.select_output_button.configure(state="normal")

        elif option == "Fill with median":
            confirm = messagebox.askyesno("Caution", "Are you sure to proceed?")
            if confirm:
                for col in self.null_counts_dict.keys():
                    if self.data_table_df[col].dtype in ['float64', 'int64']:
                        median_value = round(self.data_table_df[col].median(), 4)
                        self.data_table_df[col] = self.data_table_df[col].fillna(median_value)
                messagebox.showinfo("Filled with Median", "Null values have been filled with the median of their respective columns.")
                self.display_data(self.data_table_df)
                self.null_option_menu.configure(state="disabled")
                self.select_columns_button.configure(state="normal")
                self.select_output_button.configure(state="normal")

        elif option == "Fill with constant":
            # Habilita el campo de entrada para ingresar el valor
            self.constant_entry.place(x=60, y=203)
            self.constant_entry.configure(state="normal")
            self.constant_entry.focus()

    def hide_constant_entry(self, event=None):
        self.constant_entry.place_forget() 
        self.constant_entry.configure(state="disabled")

    def apply_constant_fill(self, event=None):
        confirm = messagebox.askyesno("Caution", "Are you sure to proceed?")
        if confirm:
            try:
                # Obtener el valor constante ingresado
                constant_value = float(self.constant_entry.get())
                self.data_table_df.fillna(constant_value, inplace=True)
                messagebox.showinfo("Filled with Constant", "Null values have been filled with the specified constant.")
                self.display_data(self.data_table_df)
                self.constant_entry.configure(state="disabled")
                self.constant_entry.delete(0, 'end')
                self.constant_entry.place_forget() 
                self.null_option_menu.configure(state="disabled")
                self.select_columns_button.configure(state="normal")
                self.select_output_button.configure(state="normal")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for the constant.")

    def select_columns(self):
        # Crear una nueva ventana para seleccionar las columnas
        self.column_window = Toplevel(self.root)
        self.column_window.title("Select Columns")
        self.column_window.configure(bg="black")
        self.column_vars = {}

        for idx, col in enumerate(self.data_table["columns"]):
            var = IntVar()
            self.column_vars[col] = var
            checkbox = ctk.CTkCheckBox(self.column_window, text=col, variable=var, text_color="white",fg_color="black")
            checkbox.pack(anchor="w")

        confirm_button = ctk.CTkButton(self.column_window, text="Confirm Selection", command=self.confirm_selection)
        confirm_button.pack(pady=10)

    def confirm_selection(self):
        self.columns_selected = [col for col, var in self.column_vars.items() if var.get() == 1]

        if self.columns_selected:
                self.input_columns_label.configure(text=f"Input Columns: {', '.join(self.columns_selected)}")
                self.column_window.destroy()
                messagebox.showinfo("Columns Selected", f"Selected columns: {', '.join(self.columns_selected)}")

        else:
            messagebox.showwarning("No Selection", "No columns selected.")

        self.column_window.destroy()

    def select_output_column(self):
        # Crear una nueva ventana para seleccionar la columna de salida
        self.output_column_window = Toplevel(self.root)
        self.output_column_window.title("Select Output Column")

        self.output_column_window.configure(bg="black")

        # Variable para almacenar la selección de columna de salida
        self.output_column_var = ctk.StringVar(value="")  # Almacena la columna seleccionada

        # Crear radiobuttons para cada columna
        for idx, col in enumerate(self.data_table["columns"]):
            radiobutton = ctk.CTkRadioButton(self.output_column_window, 
                                            text=col, 
                                            variable=self.output_column_var, 
                                            value=col,  # Cada radiobutton tiene un valor único (la columna)
                                            text_color="white",
                                            fg_color="blue",
                                            hover_color="#444444")
            radiobutton.pack(anchor="w")

        # Botón para confirmar la selección
        confirm_button = ctk.CTkButton(self.output_column_window, 
                                    text="Confirm Output Column", 
                                    command=self.confirm_output_column,
                                    fg_color="blue",
                                    text_color="white")
                                    
        confirm_button.pack(pady=10)

    def confirm_output_column(self):
        # Obtener la columna seleccionada
        selected_output_column = self.output_column_var.get()
        if selected_output_column:
            messagebox.showinfo("Output Column Selected", f"Selected Output Column: {selected_output_column}")
            self.output_column = selected_output_column  # Almacenar la columna seleccionada como atributo de clase
            self.output_column_window.destroy()
            self.output_column_label.configure(text=f"Output Column: {self.output_column}")
            self.create_model_button.configure(state="normal")

        else:
            messagebox.showwarning("No Column Selected", "Please select an output column.")

    def create_model(self):
        input_cols = self.columns_selected 
        output_col = self.output_column

        if input_cols and output_col:
            try:
                X = self.data_table_df[input_cols].values
                y = self.data_table_df[output_col].values  
                
                if not self.description_text.get():
                    messagebox.showinfo("Reminder", "No description added.")
                if np.issubdtype(X.dtype, np.number) and np.issubdtype(y.dtype, np.number):
                    model = LinearRegression()
                    model.fit(X, y)
                    if X.shape[1] == 1:  # Si hay solo una columna de entrada (regresión lineal simple)
                        self.graphic_2D(X, y, model)
                    elif X.shape[1] == 2:  # Si hay dos columnas de entrada, podemos hacer un gráfico 3D
                        self.graphic_3D(X, y, model)
                    else:
                        messagebox.showinfo("Model created", "Model created successfully, but can't plot if more than 2 inputs were selected.")

                else:
                    messagebox.showwarning("No Numeric Data!", "Columns selected must be numeric.")
            except Exception as e:
                messagebox.showerror("An Error has occurred", f"An Error has occurred while plotting model: {e}")
        else:
            messagebox.showwarning("No columns selected", "Please, select Input and Output columns.")
    
    def save_model(self):
        # Abrir un diálogo para seleccionar el archivo de modelo
        file_path = filedialog.askopenfilename(filetypes=[("PKL files", "*.pkl"), ("Joblib files", "*.joblib")])
        
        if file_path:
            try:
                if file_path.endswith(".pkl"):
                    with open(file_path, 'rb') as file:
                        model_data = pickle.load(file)
                elif file_path.endswith(".joblib"):
                    model_data = joblib.load(file_path)
                else:
                    raise ValueError("Unsupported file format.")
                
                messagebox.showinfo("Model Loaded", f"Model loaded successfully from {file_path}.")

                formula = model_data.get("formula")
                input_columns = model_data.get("input_columns")
                output_column = model_data.get("output_column")
                error_adjustment = model_data.get("error_adjustment")
                description = model_data.get("description")

                print(f"Formula: {formula}")
                print(f"Input Columns: {input_columns}")
                print(f"Output Column: {output_column}")
                print(f"Error Adjustment: {error_adjustment}")
                print(f"Description: {description}")

            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading the model: {str(e)}")
    
    def graphic_2D(self, X, y, model):
        plt.figure(figsize=(8, 6))
        
        plt.scatter(X, y, color='blue', label='Data')
        
        plt.plot(X, model.predict(X), color='red', label='Regression Line')
        
        plt.xlabel('Input')
        plt.ylabel('Output')
        plt.title('Linear regression')
        plt.legend()
        
        plt.show()

    def graphic_3D(self, X, y, model):
        try:
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')

            ax.scatter(X[:, 0], X[:, 1], y, color='b', label='Data')

            y_pred = model.predict(X)
            
            ax.plot_trisurf(X[:, 0], X[:, 1], y_pred, color='r', alpha=0.5, label='Regression Model')

            ax.set_xlabel(self.columns_selected[0])
            ax.set_ylabel(self.columns_selected[1]) 
            ax.set_zlabel(self.output_column)
            
            ax.view_init(elev=30, azim=45)  

            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')

            ax.grid(True, color='gray', linestyle='-', linewidth=0.5)
            ax.tick_params(axis='both', direction='in', length=6, width=1, colors='white')

            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting 3D data: {str(e)}")
    
    def model_description(self):
        self.description = self.description_text.get()

        if not self.description:
            messagebox.showinfo("Reminder", "No description added.")
        else:
            messagebox.showinfo("Reminder", "Description added successfully.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = GUI(root)
    root.mainloop()