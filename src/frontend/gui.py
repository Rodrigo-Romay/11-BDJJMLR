import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from backend.read_file import DataImport
from backend.preprocess import Preprocess
from backend.model import Model
from backend.columns import Columns
from backend.predictions import Predictions


# ==================================== GUI ==================================

class GUI:
    """Graphical User Interface for the Trendify application.

    This class defines the layout and behavior of the application, including
    widgets, event handling, and interactions between components.
    """

    def __init__(self, root):
        """Initializes the GUI class and sets up the main application window.

        Args:
            root (tk.Tk): The root window of the application.
        """

        self.root = root
        self.root.title("Trendify")
        self._file = None
        self.columns_selected = []
        self.columns_select = None
        self.output_column = None
        self.data_table_df = None
        self.description_saved = ""

        # Configure the window
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Layout configuration
        self.root.grid_columnconfigure(0, weight=1, minsize=450)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=6)

        self.create_widgets()

    # ------------------------------- LABEL ----------------------------

    def create_label(self, master, text, font, text_color="#333333"):
        """Creates a label widget.

        Args:
            master (tk.Widget): Parent widget for the label.
            text (str): The text to display on the label.
            font (tuple): Font style for the label.
            text_color (str, optional): Color of the text. Defaults to "#333333".

        Returns:
            ctk.CTkLabel: A custom tkinter label widget.
        """

        label = ctk.CTkLabel(
            master,
            text=text,
            font=font,
            text_color=text_color
        )
        return label

    # ------------------------------- LOADING SCREEN ----------------------------

    def create_loading_screen(self):
        """Creates a loading screen with a progress bar.

        The loading screen is initially hidden and includes a label to indicate
        the loading process and a progress bar to show progress dynamically.
        """

        self.loading_frame = ctk.CTkFrame(
            self.root, fg_color="white", corner_radius=15)
        self.loading_frame.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.loading_frame.grid_forget()  # Initially hidden

        self.loading_label = self.create_label(
            self.loading_frame, "Loading...", font=("Roboto", 30, "bold"), text_color="grey")
        self.loading_label.pack(pady=90)

        self.progress_bar = ctk.CTkProgressBar(self.loading_frame, width=300)
        self.progress_bar.pack(pady=20)

    def show_loading_screen(self):
        """Displays the loading screen and starts the progress bar animation."""

        self.loading_frame.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.progress_bar.set(0)
        self.progress_bar.start()

    def hide_loading_screen(self):
        """Hides the loading screen and stops the progress bar animation."""

        self.loading_frame.grid_forget()
        self.progress_bar.stop()

    # ------------------------------- FRAMES ----------------------------

    def create_widgets(self):
        """Creates and initializes all widgets in the application."""

        self.create_title_bar()
        self.create_sidebar()
        self.create_main_section()
        self.create_bottom_section()
        self.create_loading_screen()

    def create_title_bar(self):
        """Creates the top title bar with the application name and subtitle."""

        self.title_bar = ctk.CTkFrame(
            self.root, fg_color="#2c3e50", height=50, corner_radius=0)
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
        """Creates a sidebar with action buttons and null-handling options."""

        #------------------------- Frames ----------------------

        self.sidebar = ctk.CTkFrame(
            self.root, fg_color="white", corner_radius=15)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        button_frame = ctk.CTkFrame(
            self.sidebar, fg_color="white", corner_radius=15)
        button_frame.pack(pady=10, fill="x", padx=10)

        #------------------- Button Style -------------------------

        button_style = {
            "corner_radius": 8,
            "fg_color": "#3498db",
            "hover_color": "#2980b9",
            "text_color": "white",
            "font": ("Roboto", 14, "bold")
        }

        #----------------------- Buttons -----------------------

        #Make new model
        self.make_new_model = ctk.CTkButton(
            button_frame,
            text="Make new Model",
            command=self.make_new_model_preset,
            **button_style
        )
        self.make_new_model.configure(
            fg_color="#718093", hover_color="#b2bec3")
        self.make_new_model.pack(side="left", expand=True, padx=5)

        #Load model
        self.load_model_button = ctk.CTkButton(
            button_frame,
            text="Load Model",
            command=self.load_model,
            **button_style
        )
        self.load_model_button.configure(
            fg_color="#718093", hover_color="#b2bec3")
        self.load_model_button.pack(side="left", expand=True, padx=5)

        #Load
        self.load_button = ctk.CTkButton(
            self.sidebar,
            text="Open File",
            command=self.load_file,
            **button_style
        )
        self.load_button.configure(fg_color="#A2B0C1", hover_color="#D4DDE1")
        self.load_button.pack(pady=5, fill="x", padx=10)
        self.load_button.configure(state="disabled")
        self.load_button.pack_forget()

        #Preprocess data
        self.preprocess_button = ctk.CTkButton(
            self.sidebar,
            text="Preprocess Data",
            command=self.preprocess_data,
            **button_style
        )
        self.preprocess_button.pack(pady=5, fill="x", padx=10)
        self.preprocess_button.configure(state="disabled")
        self.preprocess_button.pack_forget()

        #Null option menu
        self.null_handling_frame = ctk.CTkFrame(
            self.sidebar, fg_color="#f5f5f5", corner_radius=10)
        self.null_handling_frame.pack(pady=20, fill="x", padx=10)
        self.null_handling_frame.pack_forget()

        self.null_handling_label = self.create_label(
            self.null_handling_frame,
            "Handle Null Values:",
            font=("Roboto", 14, "bold"),
            text_color="#34495e"
        )
        self.null_handling_label.pack(pady=5)
        self.null_handling_label.pack_forget()

        self.null_handling_option = ctk.StringVar(value="Select an option")

        self.null_option_menu = ctk.CTkOptionMenu(
            self.null_handling_frame,
            variable=self.null_handling_option,
            values=["Delete rows with nulls", "Fill with mean",
                    "Fill with median", "Fill with constant"],
            command=self.handle_null_option,
            button_color="#2ecc71",
            button_hover_color="#27ae60",
            fg_color="#ecf0f1",
            text_color="#34495e",
            dropdown_fg_color="white",
            dropdown_hover_color="#ecf0f1",
            dropdown_text_color="#2c3e50",
            corner_radius=10
        )
        self.null_option_menu.pack(pady=5, fill="x")
        self.null_option_menu.configure(state="disabled")
        self.null_option_menu.pack_forget()

        self.constant_entry = ctk.CTkEntry(
            self.null_handling_frame,
            placeholder_text="Enter constant",
            font=("Roboto", 12),
            corner_radius=8
        )
        self.constant_entry.pack(pady=5, fill="x")
        self.constant_entry.configure(state="disabled")
        self.constant_entry.pack_forget()

        #Select input columns
        self.select_columns_button = ctk.CTkButton(
            self.sidebar,
            text="Select Input Columns",
            command=self.select_columns,
            **button_style
        )
        self.select_columns_button.pack(pady=5, fill="x", padx=10)
        self.select_columns_button.configure(state="disabled")
        self.select_columns_button.pack_forget()

        #Select output column
        self.select_output_button = ctk.CTkButton(
            self.sidebar,
            text="Select Output Column",
            command=self.select_output_column,
            **button_style
        )
        self.select_output_button.pack(pady=5, fill="x", padx=10)
        self.select_output_button.configure(state="disabled")
        self.select_output_button.pack_forget()

        #Create model
        self.create_model_button = ctk.CTkButton(
            self.sidebar,
            text="Create Model",
            command=self.create_model,
            **button_style
        )
        self.create_model_button.pack(pady=5, fill="x", padx=10)
        self.create_model_button.configure(state="disabled")
        self.create_model_button.pack_forget()

        #Show model
        self.show_model_button = ctk.CTkButton(
            self.sidebar,
            text="Show Model",
            command=self.show_model,
            **button_style
        )
        self.show_model_button.pack(pady=5, fill="x", padx=10)
        self.show_model_button.configure(state="disabled")
        self.show_model_button.pack_forget()

        #Predict
        self.predict_button = ctk.CTkButton(
            self.sidebar,
            text="Make Prediction",
            command=self.make_predictions,
            **button_style
        )

        self.predict_button.pack(pady=5, fill="x", padx=10)
        self.predict_button.configure(state="disabled")
        self.predict_button.pack_forget()

        #Save
        self.save_button = ctk.CTkButton(
            self.sidebar,
            text="Save Model",
            command=self.save_model,
            **button_style
        )

        self.save_button.configure(fg_color="#4d6a86", hover_color="#3f556b")
        self.save_button.pack(pady=5, fill="x", padx=10)
        self.save_button.configure(state="disabled")
        self.save_button.pack_forget()

        self.model = Model(self.save_button, self.load_model_button, self.predict_button, self.show_model_button,
                           self.preprocess_button, self.select_columns_button, self.select_output_button, self.null_option_menu,
                           self.create_model_button, self.constant_entry, self.null_handling_label, self.null_handling_frame, self.load_button)

    def create_main_section(self):
        """Creates the main content section of the application."""

        #------------------------- Frames ----------------------

        self.main_section = ctk.CTkFrame(
            self.root, fg_color="white", corner_radius=15)
        self.main_section.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.main_section.grid_rowconfigure(0, weight=1)
        self.main_section.grid_columnconfigure(0, weight=1)

        self.table_frame = ctk.CTkFrame(
            self.main_section, corner_radius=15, fg_color="white")
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #----------------- Data table / Scrollbars ----------------

        self.x_scrollbar = ttk.Scrollbar(
            self.table_frame, orient="horizontal", style="Custom.Horizontal.TScrollbar")
        self.x_scrollbar.pack(side="bottom", fill="x")

        self.y_scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", style="Custom.Vertical.TScrollbar")
        self.y_scrollbar.pack(side="right", fill="y")

        self.data_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set
        )
        self.data_table.pack(fill="both", expand=True)

        self.x_scrollbar.config(command=self.data_table.xview)
        self.y_scrollbar.config(command=self.data_table.yview)

        #Data table style
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 12),
                        background="white", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", font=(
            "Roboto", 14, "bold"), background="#dfe6e9", foreground="black")
        style.map("Treeview", background=[("selected", "#b2bec3")], foreground=[
                  ("selected", "#ffffff")])

        #Scrollbars style
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
        """Creates the bottom section for displaying summaries and statistics."""

        #------------------------- Frames ----------------------

        self.bottom_section = ctk.CTkFrame(
            self.root, fg_color="white", corner_radius=15)
        self.bottom_section.grid(
            row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.bottom_section.grid_columnconfigure(0, minsize=450)
        self.bottom_section.grid_columnconfigure(1, minsize=400)
        self.bottom_section.grid_columnconfigure(2, minsize=650)
        self.bottom_section.grid_columnconfigure(3, minsize=200)
        self.bottom_section.grid_rowconfigure(0, weight=0)
        self.bottom_section.grid_rowconfigure(1, weight=1)
        self.bottom_section.grid_rowconfigure(2, weight=0)

        #------------------------- Labels ----------------------

        #Formula
        self.formula_label = self.create_label(
            self.bottom_section,
            "Formula: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.formula_label.grid(
            row=0, column=1, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        #MSE
        self.mse_label = self.create_label(
            self.bottom_section,
            "MSE: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.mse_label.grid(row=1, column=1, sticky="w", padx=10, pady=(5, 5))

        #R2
        self.r2_label = self.create_label(
            self.bottom_section,
            "R2: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.r2_label.grid(row=2, column=1, sticky="w", padx=10, pady=(5, 5))

        #Result prediction
        self.result_prediction_label = self.create_label(
            self.bottom_section,
            text="Result prediction: None",
            font=("Roboto", 14),
            text_color="#A0A0A0"
        )
        self.result_prediction_label.grid(
            row=2, column=3, sticky="w", padx=10, pady=(5, 10))

        #Description entry
        self.description_label = self.create_label(
            self.bottom_section,
            text="Model Description:",
            font=("Roboto", 14),
            text_color="black"
        )
        self.description_label.grid(
            row=0, column=0, sticky="w", padx=10, pady=(5, 2))

        self.description_entry = ctk.CTkEntry(
            self.bottom_section,
            placeholder_text="Enter description here...",
            width=275
        )
        self.description_entry.grid(
            row=1, column=0, sticky="w", padx=10, pady=(2, 5))

        self.save_description_button = ctk.CTkButton(
            self.bottom_section,
            text="Save Description",
            command=self.save_description,
            corner_radius=8,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            text_color="white"
        )
        self.save_description_button.grid(
            row=2, column=0, sticky="w", padx=10, pady=(2, 5))

        #Description loaded
        self.load_description_label = self.create_label(
            self.bottom_section,
            "Description: None",
            ("Roboto", 14),
            "#A0A0A0",
        )
        self.load_description_label.grid(
            row=1, column=3, sticky="w", padx=10, pady=(5, 10))

        #File path
        self.file_path_label = self.create_label(
            self.bottom_section,
            text="File Path: No file loaded",
            font=("Roboto", 14),
            text_color="#A0A0A0"
        )
        self.file_path_label.grid(
            row=0, column=3, sticky="w", padx=10, pady=(10, 5))

        #Input columns
        self.input_columns_label = self.create_label(
            self.bottom_section,
            "Input Columns: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.input_columns_label.grid(
            row=1, column=2, sticky="w", padx=10, pady=(5, 5))

        #Output column
        self.output_column_label = self.create_label(
            self.bottom_section,
            "Output Column: None",
            ("Roboto", 14),
            "#A0A0A0"
        )
        self.output_column_label.grid(
            row=2, column=2, sticky="w", padx=10, pady=(5, 5))

    #------------------------------- LOAD FILE ------------------------------

    def load_file(self):
        """Loads a data file selected by the user and displays it in the table."""

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
                    
                    #------------------ If data is not empty ------------------

                    self.show_loading_screen()
                    self.data_table["show"] = "headings"
                    self.data_table_df = data
                    self.display_data(data)

                    self.mse_label.configure(text="MSE: None")
                    self.r2_label.configure(text="R2: None")
                    self.formula_label.configure(text="Formula: None")
                    self.input_columns_label.configure(
                        text="Input Columns: None")
                    self.output_column_label.configure(
                        text="Output Column: None")
                    self.result_prediction_label.configure(
                        text="Result prediction: None")
                    self.load_description_label.configure(
                        text="Description: None")

                    self.preprocess_button.configure(state="normal")
                    self.null_option_menu.configure(state="disabled")
                    self.constant_entry.configure(state="disabled")
                    self.constant_entry.pack_forget()
                    self.select_columns_button.configure(state="disabled")
                    self.select_output_button.configure(state="disabled")
                    self.create_model_button.configure(state="disabled")
                    self.show_model_button.configure(state="disabled")
                    self.predict_button.configure(state="disabled")
                    self.save_button.configure(state="disabled")

                    self.columns_selected = []
                    self.output_column = None
                    self.file_path_label.configure(
                        text=f"File loaded: {self._file}")
                else:

                    #------------------ If data is empty -----------------------

                    self.data_table.delete(*self.data_table.get_children())
                    self.data_table["show"] = "tree"

                    self.mse_label.configure(text="MSE: None")
                    self.r2_label.configure(text="R2: None")
                    self.formula_label.configure(text="Formula: None")
                    self.file_path_label.configure(
                        text="File Path: No file loaded")
                    self.input_columns_label.configure(
                        text="Input Columns: None")
                    self.output_column_label.configure(
                        text="Output Column: None")
                    self.result_prediction_label.configure(
                        text="Result prediction: None")
                    self.load_description_label.configure(
                        text="Description: None")

                    self.preprocess_button.configure(state="disabled")
                    self.null_option_menu.configure(state="disabled")
                    self.constant_entry.configure(state="disabled")
                    self.select_columns_button.configure(state="disabled")
                    self.select_output_button.configure(state="disabled")
                    self.create_model_button.configure(state="disabled")
                    self.show_model_button.configure(state="disabled")
                    self.predict_button.configure(state="disabled")
                    self.save_button.configure(state="disabled")

                    messagebox.showerror(
                        "Error", "No data to display. Please check the file.")
            except Exception as e:
                messagebox.showerror("Error", f"Error while loading file: {e}")
        self.root.after(600, self.hide_loading_screen)

    #---------------------------- DISPLAY DATA -----------------------------

    def display_data(self, data):
        """Populates the table view with the provided data.

        Args:
            data (DataFrame): The data to be displayed in the table.
        """

        self.data_table.delete(*self.data_table.get_children())
        self.data_table["columns"] = list(data.columns)

        for col in data.columns:
            self.data_table.heading(col, text=col, anchor="center")
            self.data_table.column(col, anchor="center")
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))

    #------------------------- AUXILIAR FUNCTIONS ---------------------------------

    def make_new_model_preset(self):
        """Resets the application to the initial state, preparing it for creating a new model."""

        self.data_table.delete(*self.data_table.get_children())
        self.data_table["show"] = "tree"

        self.mse_label.configure(text="MSE: None")
        self.r2_label.configure(text="R2: None")
        self.formula_label.configure(text="Formula: None")
        self.file_path_label.configure(text="File Path: No file loaded")
        self.input_columns_label.configure(text="Input Columns: None")
        self.output_column_label.configure(text="Output Column: None")
        self.result_prediction_label.configure(text="Result prediction: None")
        self.load_description_label.configure(text="Description: None")

        if self.predict_button.cget("state") == "normal":
            self.predict_button.pack_forget()

        self.load_button.pack(pady=5, fill="x", padx=10)
        self.preprocess_button.pack(pady=5, fill="x", padx=10)
        self.null_handling_frame.pack(pady=20, fill="x", padx=10)
        self.null_handling_label.pack(pady=5)
        self.null_option_menu.pack(pady=5, fill="x")
        self.select_columns_button.pack(pady=5, fill="x", padx=10)
        self.select_output_button.pack(pady=5, fill="x", padx=10)
        self.create_model_button.pack(pady=5, fill="x", padx=10)
        self.show_model_button.pack(pady=5, fill="x", padx=10)
        self.predict_button.pack(pady=5, fill="x", padx=10)
        self.save_button.pack(pady=5, fill="x", padx=10)

        self.load_button.configure(state="normal")
        self.preprocess_button.configure(state="disabled")
        self.null_option_menu.configure(state="disabled")
        self.constant_entry.configure(state="disabled")
        self.select_columns_button.configure(state="disabled")
        self.select_output_button.configure(state="disabled")
        self.create_model_button.configure(state="disabled")
        self.show_model_button.configure(state="disabled")
        self.predict_button.configure(state="disabled")
        self.save_button.configure(state="disabled")

    def handle_null_option(self, option):
        """Handles the null values based on the option selected by the user.

        Args:
            option (str): The selected option for handling null values.
        """

        self.show_loading_screen()
        self.preprocess.handle_null_option(option)
        self.root.after(500, self.hide_loading_screen)

    def preprocess_data(self):
        """Prepares the loaded dataset for further processing, including handling null values."""

        self.preprocess = Preprocess(self.data_table_df, self.null_option_menu, self.display_data,
                                     self.constant_entry, self.select_columns_button, self.select_output_button, self.preprocess_button, self.root)
        self.preprocess.preprocess_data()

    def hide_constant_entry(self):
        """Hides the constant entry field for filling missing values."""

        self.preprocess.hide_constant_entry()

    def apply_constant_fill(self):
        """Applies the user-specified constant value to fill missing data in the dataset."""

        self.preprocess.apply_constant_fill()

    def select_columns(self):
        """Opens the column selection interface to allow the user to select input columns."""

        if not self.columns_select:
            self.columns_select = Columns(
                self.root, self.data_table, self.input_columns_label, self.output_column_label, self.create_model_button)
        self.columns_select.select_columns()

    def select_output_column(self):
        """Opens the interface for selecting the output column from the dataset."""

        if self.columns_select:
            self.columns_select.select_output_column()

    def get_selected_columns(self):
        """Retrieves the user-selected input and output columns."""

        self.columns_selected = self.columns_select.columns_selected
        self.output_column = self.columns_select.output_column

    def create_model(self):
        """Creates a predictive model using the selected columns and displays the resulting formula."""

        self.get_selected_columns()
        self.model.create_model(self.columns_selected, self.output_column,
                                self.data_table_df, self.formula_label, self.mse_label, self.r2_label)
        self.formula = self.model.model_formula

    def show_model(self):
        """Plots and visualizes the collected information about the created model."""

        self.model.show_model()

    def save_model(self):
        """Saves the created predictive model to a file."""

        self.model.save_model()

    def make_predictions(self):
        """Performs predictions using the trained model and displays the results."""

        self.predictions = Predictions(
            self.formula, self.root, self.result_prediction_label)
        self.predictions.predictions()

    def load_model(self):
        """Loads a previously saved predictive model and updates the application state accordingly."""

        self.model.load_model(self.input_columns_label, self.output_column_label, self.formula_label, self.load_description_label,
                              self.mse_label, self.r2_label, self.result_prediction_label, self.file_path_label, self.data_table)
        self.formula = self.model.model_formula

    def save_description(self):
        """Saves the user-provided description for the model and updates the UI."""

        description = self.description_entry.get()
        self.model.save_description(description, self.load_description_label)
