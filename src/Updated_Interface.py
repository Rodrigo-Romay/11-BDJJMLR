import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from read_file import DataImport
from preprocess_updated_interface2 import Preprocess
from model_updated_interface2 import Model
from columns_updated_interface2 import Columns


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trendify")
        self._file = None
        self.columns_selected = []
        self.output_column = None
        self.data_table_df = None
        self.description_saved = ""

        # Configure the window
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Layout configuration
        self.root.grid_columnconfigure(0, weight=1, minsize=300)  # Sidebar
        self.root.grid_columnconfigure(1, weight=3)  # Main content
        self.root.grid_rowconfigure(0, weight=1)  # Title
        self.root.grid_rowconfigure(1, weight=6)  # Main content

        self.create_widgets()

    def create_label(self, master, text, font, text_color="#333333"):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=font,
            text_color=text_color
        )
        return label

    def create_widgets(self):
        self.create_title_bar()
        self.create_sidebar()
        self.create_main_section()
        self.create_bottom_section()

    def create_title_bar(self):
        """Top title bar with the app name."""
        self.title_bar = ctk.CTkFrame(self.root, fg_color="#2c3e50", height=50, corner_radius=0)
        self.title_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.title_label = self.create_label(
            self.title_bar,
            "Trendify",
            font=("Pacifico", 30, "bold"),
            text_color="white"
        )
        self.title_label.pack(side="left", padx=20)

        self.subtitle_label = self.create_label(
            self.title_bar,
            "Data Analysis & Model Builder",
            font=("Roboto", 16),
            text_color="#ecf0f1"
        )
        self.subtitle_label.pack(side="left", padx=10)

    def create_sidebar(self):
        """Sidebar with action buttons and null-handling options."""
        self.sidebar = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Add buttons to the sidebar
        button_style = {
            "corner_radius": 8,
            "fg_color": "#3498db",
            "hover_color": "#2980b9",
            "text_color": "white",
            "font": ("Roboto", 14, "bold")
        }

        self.load_button = ctk.CTkButton(
            self.sidebar,
            text="OPEN FILE",
            command=self.load_file,
            **button_style
        )
        self.load_button.configure(fg_color="#718093", hover_color="#b2bec3")
        self.load_button.pack(pady=10, fill="x", padx=10)

        self.preprocess_button = ctk.CTkButton(
            self.sidebar,
            text="Preprocess Data",
            command=self.preprocess_data,
            **button_style
        )
        self.preprocess_button.pack(pady=10, fill="x", padx=10)
        self.preprocess_button.configure(state="disabled")

        # Null-handling section
        self.null_handling_frame = ctk.CTkFrame(self.sidebar, fg_color="#f5f5f5", corner_radius=10)
        self.null_handling_frame.pack(pady=20, fill="x", padx=10)

        self.null_handling_label = self.create_label(
            self.null_handling_frame,
            "Handle Missing Values:",
            font=("Roboto", 14, "bold"),
            text_color="#34495e"
        )
        self.null_handling_label.pack(pady=5)

        self.null_handling_option = ctk.StringVar(value="Select an option")

        self.null_option_menu = ctk.CTkOptionMenu(
            self.null_handling_frame,
            variable=self.null_handling_option,
            values=["Delete rows with nulls", "Fill with mean",
                    "Fill with median", "Fill with constant"],
            command=self.handle_null_option,
            button_color="#2ecc71",
            fg_color="#ecf0f1",
            text_color="#34495e",
            corner_radius=8,
        )
        self.null_option_menu.pack(pady=10, fill="x")
        self.null_option_menu.configure(state="disabled")

        self.constant_entry = ctk.CTkEntry(
            self.null_handling_frame,
            placeholder_text="Enter constant",
            font=("Roboto", 12),
            corner_radius=8
        )
        self.constant_entry.pack(pady=10, fill="x")
        self.constant_entry.configure(state="disabled")
        self.constant_entry.pack_forget()
        self.constant_entry.bind("<Return>", self.apply_constant_fill)
        self.root.bind("<Escape>", self.hide_constant_entry)

        self.select_columns_button = ctk.CTkButton(
            self.sidebar,
            text="Select Input Columns",
            command=self.select_columns,
            **button_style
        )
        self.select_columns_button.pack(pady=10, fill="x", padx=10)
        self.select_columns_button.configure(state="disabled")

        self.select_output_button = ctk.CTkButton(
            self.sidebar,
            text="Select Output Column",
            command=self.select_output_column,
            **button_style
        )
        self.select_output_button.pack(pady=10, fill="x", padx=10)
        self.select_output_button.configure(state="disabled")

        self.create_model_button = ctk.CTkButton(
            self.sidebar,
            text="Create Model",
            command=self.create_model,
            **button_style
        )
        self.create_model_button.pack(pady=10, fill="x", padx=10)
        self.create_model_button.configure(state="disabled")

        self.save_button = ctk.CTkButton(
            self.sidebar,
            text="Save Model",
            command=self.save_model,
            **button_style
        )
        self.model = Model(self.save_button)

        self.save_button.pack(pady=10, fill="x", padx=10)
        self.save_button.configure(state="disabled")

    def create_main_section(self):
        """Main section with the data table and scrollbars."""
        self.main_section = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15)
        self.main_section.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Configure grid inside main section
        self.main_section.grid_rowconfigure(0, weight=1)
        self.main_section.grid_columnconfigure(0, weight=1)

        # Frame for the table and scrollbars
        self.table_frame = ctk.CTkFrame(self.main_section, corner_radius=15, fg_color="white")
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Scrollbars for the table
        self.x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", style="Custom.Horizontal.TScrollbar")
        self.x_scrollbar.pack(side="bottom", fill="x")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", style="Custom.Vertical.TScrollbar")
        self.y_scrollbar.pack(side="right", fill="y")

        # Table setup with scrollbars
        self.data_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set
        )
        self.data_table.pack(fill="both", expand=True)

        # Configuring scrollbars to work with the table
        self.x_scrollbar.config(command=self.data_table.xview)
        self.y_scrollbar.config(command=self.data_table.yview)

        # Styling the table
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 12), background="white", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", font=("Roboto", 14, "bold"), background="#dfe6e9", foreground="black")
        style.map("Treeview", background=[("selected", "#b2bec3")], foreground=[("selected", "#ffffff")])

        # Styling the scrollbars
        style.configure(
            "Custom.Horizontal.TScrollbar",
            gripcount=0,
            background="#ecf0f1",
            darkcolor="#bdc3c7",
            lightcolor="#ecf0f1",
            troughcolor="#ffffff",
            bordercolor="#dfe6e9",
            arrowcolor="#7f8c8d",
            relief="flat"
        )

        style.configure(
            "Custom.Vertical.TScrollbar",
            gripcount=0,
            background="#ecf0f1",
            darkcolor="#bdc3c7",
            lightcolor="#ecf0f1",
            troughcolor="#ffffff",
            bordercolor="#dfe6e9",
            arrowcolor="#7f8c8d",
            relief="flat"
        )

    def create_bottom_section(self):
        """Bottom section with description, file info, and column selections."""
        self.bottom_section = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15)
        self.bottom_section.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        # === Etiqueta para descripción del modelo ===
        self.description_label = self.create_label(
            self.bottom_section,
            text="Model Description:",
            font=("Roboto", 14),
            text_color="black"
        )
        self.description_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 2))

        # === Entrada de descripción ===
        self.description_entry = ctk.CTkEntry(
            self.bottom_section,
            placeholder_text="Enter description here...",
            width=600
        )
        self.description_entry.grid(row=1, column=0, sticky="w", padx=10, pady=(2, 5))

        # === Botón para guardar descripción ===
        self.save_description_button = ctk.CTkButton(
            self.bottom_section,
            text="Save Description",
            command=self.save_description,
            corner_radius=8,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            text_color="white"
        )
        self.save_description_button.grid(row=2, column=0, sticky="w", padx=10, pady=(2, 5))

        # === Etiqueta para mostrar la ruta del archivo ===
        self.file_path_label = ctk.CTkLabel(
            self.bottom_section,
            text="No file loaded",
            font=("Roboto", 12),
            text_color="#7f8c8d"
        )
        self.file_path_label.grid(row=3, column=0, sticky="w", padx=10, pady=7)

        # === Etiquetas para columnas de entrada y salida ===
        self.input_columns_label = self.create_label(
            self.bottom_section,
            "Input Columns: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.input_columns_label.grid(row=4, column=0, sticky="w", padx=10, pady=7)

        self.output_column_label = self.create_label(
            self.bottom_section,
            "Output Column: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.output_column_label.grid(row=4, column=1, sticky="w", padx=10, pady=(2, 2))

        # Configuración de las columnas y filas
        self.bottom_section.grid_columnconfigure(0, weight=1)
        self.bottom_section.grid_columnconfigure(1, weight=1)
        self.bottom_section.grid_rowconfigure(5, weight=0)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files",
                                                "*.xlsx *.xls"), ("SQLite Files", "*.db *.sqlite")]
        )
        if file_path:
            self._file = file_path
            try:
                data_importer = DataImport(self._file)
                data_importer.file_type()
                data = data_importer._data
                if not data.empty:
                    self.data_table_df = data
                    self.display_data(data)
                    self.preprocess_button.configure(state="normal")
                    self.null_option_menu.configure(state="disabled")
                    self.select_columns_button.configure(state="disabled")
                    self.select_output_button.configure(state="disabled")
                    self.columns_selected = []
                    self.output_column = None
                    # Update file path label
                    self.file_path_label.configure(text=f"File loaded: {self._file}")
                else:
                    self.data_table.delete(*self.data_table.get_children())
                    messagebox.showerror("Error", "No data to display. Please check the file.")
            except Exception as e:
                messagebox.showerror("Error", f"Error while loading file: {e}")

    def display_data(self, data):
        self.data_table.delete(*self.data_table.get_children())
        self.data_table["columns"] = list(data.columns)
        for col in data.columns:
            self.data_table.heading(col, text=col, anchor="center")
            self.data_table.column(col, anchor="center")
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))

    def handle_null_option(self, option):
        self.preprocess.handle_null_option(option)

    def preprocess_data(self):
        self.preprocess = Preprocess(self.data_table_df, self.null_option_menu, self.display_data,
                                     self.constant_entry, self.select_columns_button, self.select_output_button, self.preprocess_button)
        self.preprocess.preprocess_data()

    def hide_constant_entry(self):
        self.preprocess.hide_constant_entry()

    def apply_constant_fill(self):
        self.preprocess.apply_constant_fill()

    def select_columns(self):
        self.columns_select = Columns(self.root, self.data_table, self.input_columns_label, self.output_column_label, self.create_model_button)
        self.columns_select.select_columns()

    def select_output_column(self):
        self.columns_select.select_output_column()

    def get_selected_columns(self):
        self.columns_selected = self.columns_select.columns_selected
        self.output_column = self.columns_select.output_column

    def create_model(self):
        self.get_selected_columns()
        self.model.create_model(columns_selected=self.columns_selected,output_column=self.output_column, data_table_df=self.data_table_df)

    def save_model(self):
        self.model.save_model()

    def save_description(self):
        description = self.description_entry.get()
        self.model.save_description(description)
