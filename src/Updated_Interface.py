import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, IntVar
from tkinter import ttk
from Modulo import DataImport
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import joblib
from preprocess_updated_interface import Preprocess
from columns_updated_interface import Columns
from model_updated_interface import Model

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Preprocessing Dataset")
        self._file = None
        self.columns_selected = []
        self.output_column = None
        self.data_table_df = None
        self.description_saved = ""
        self.model_formula = {}
        self.model_metrics = {}
        self.model = None  
        self.create_widgets()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")
    
    def create_label(self, master, text, font, text_color="#A0A0A0" ):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=font,
            text_color=text_color
        )
        return label


    def create_widgets(self):
        self.create_title_label()
        self.create_file_section()
        self.create_table_section()
        self.create_features_section()
        self.create_preprocess_section()
        self.create_columns_selection_section()    
        self.create_model_section()
        self.create_description_section()

    def create_title_label(self):
        self.title_label = self.create_label(self.root, "Preprocessing Dataset", ("Roboto", 24, "bold"), "black")
        self.title_label.pack(pady=10)
    
    def create_file_section(self):
        self.load_button = ctk.CTkButton(self.root, text="OPEN FILE", command=self.load_file, corner_radius=8,
                                         fg_color="#ffcc00", hover_color="#ffb700",text_color="black", font=("Roboto", 14, "bold"))
        self.load_button.pack(pady=10)

        self.file_label = self.create_label(self.root, "", ("Roboto", 12), "gray")
        self.file_label.pack()

    def create_table_section(self):
        self.table_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="white")
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.data_table = ttk.Treeview(self.table_frame, show="headings")
        self.data_table.pack(expand=True, fill="both")

        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 12), background="white", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", font=("Roboto", 14, "bold"), background="#e6e6e6", foreground="black")

    def create_features_section(self):
        self.features_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.features_frame.pack(pady=5, fill="x")

        self.input_columns_label = self.create_label(self.features_frame, "Features: None", ("Roboto", 14), "black")
        self.input_columns_label.pack(side="left", padx=(20, 5))

        self.output_column_label = self.create_label(self.features_frame, "Target: None", ("Roboto", 14), "black")
        self.output_column_label.pack(side="left", padx=5)

    def create_preprocess_section(self):
        self.preprocess_button = ctk.CTkButton(self.root, text="Preprocess Data", command=self.preprocess_data, corner_radius=8,
                                               fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.preprocess_button.pack(pady=10)
        self.preprocess_button.configure(state="disabled")

        self.null_option_label = self.create_label(self.root, text="Handle Null Values:", font=("Roboto", 14), text_color="black")
        self.null_option_label.pack(pady=5)

        self.null_handling_option = ctk.StringVar(value="Select Option")
        self.null_option_menu = ctk.CTkOptionMenu(self.root, variable=self.null_handling_option,
                                                  values=["Delete rows with nulls", "Fill with mean", "Fill with median", "Fill with constant"],
                                                  button_color="#0078d7", text_color="white", fg_color="white", corner_radius=5,
                                                  command=self.handle_null_option)
        self.null_option_menu.pack(pady=5)
        self.null_option_menu.configure(state="disabled")

        self.constant_entry = ctk.CTkEntry(self.root, placeholder_text="Constant Value", width=200)
        self.constant_entry.pack(pady=5)
        self.constant_entry.configure(state="disabled")

    def create_columns_selection_section(self):    
        self.select_columns_button = ctk.CTkButton(self.root, text="Select Input Columns", command=self.select_columns, corner_radius=8,
                                                   fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.select_columns_button.pack(pady=10)
        self.select_columns_button.configure(state="disabled")

        self.select_output_button = ctk.CTkButton(self.root, text="Select Output Column", command=self.select_output_column, corner_radius=8,
                                                  fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.select_output_button.pack(pady=10)
        self.select_output_button.configure(state="disabled")
    
    def create_model_section(self):
        self.create_model_button = ctk.CTkButton(self.root, text="Create Model", command=self.create_model, corner_radius=8,
                                                 fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.create_model_button.pack(pady=10)
        self.create_model_button.configure(state="disabled")

        self.save_button = ctk.CTkButton(self.root, text="Save Model", command=self.save_model, corner_radius=8,
                                         fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.save_button.pack(pady=10)
        self.save_button.configure(state="disabled")
    
    def create_description_section(self):
        self.description_label = self.create_label(self.root, text="Model Description:", font=("Roboto", 14), text_color="black")
        self.description_label.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self.root, placeholder_text="Enter description here...", width=400)
        self.description_entry.pack(pady=5)

        self.save_description_button = ctk.CTkButton(self.root, text="Save Description", command=self.save_description, corner_radius=8,
                                                     fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.save_description_button.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("SQLite Files", "*.db *.sqlite")]
        )
        if file_path:
            self._file = file_path
            self.file_label.configure(text=f"File: {self._file}")
            try:
                data_importer = DataImport(self._file)
                data_importer.file_type()
                data = data_importer._data
                if not data.empty:
                    self.data_table_df = data
                    self.display_data(data)
                    self.preprocess_button.configure(state="normal")
                    self.select_columns_button.configure(state="normal")
                    self.select_output_button.configure(state="normal")
                    self.columns_selected = []
                    self.output_column = None
                    self.input_columns_label.configure(text="Features: None")
                    self.output_column_label.configure(text="Target: None")
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

    def preprocess_data(self):
        self.preprocess = Preprocess(self.data_table_df,self.null_option_menu,self.display_data,self.constant_entry, self.preprocess_button)
        self.preprocess.preprocess_data()

    def handle_null_option(self, option):
        self.preprocess.handle_null_option(option)

    def fill_with_constant(self, event=None):
        self.preprocess.fill_with_constant()

    def select_columns(self):
        self.select_columns_input = Columns(self.root,self.data_table,self.input_columns_label,self.output_column_label, self.create_model_button)
        self.select_columns_input.select_columns()

    def select_output_column(self):
        self.output_column_select = Columns(self.root,self.data_table,self.input_columns_label,self.output_column_label, self.create_model_button)
        self.output_column_select.select_output_column()

    def get_selected_columns(self):
        self.columns_selected =  self.select_columns_input.columns_selected
        self.output_column =  self.output_column_select.output_column

    def save_description(self):
        self.description_saved = self.description_entry.get()
        if self.description_saved:
            messagebox.showinfo("Success", "Description saved successfully!")
        else:
            messagebox.showwarning("Warning", "Description is empty. Please enter a description.")

    def create_model(self):
        self.model = Model(self.save_button)
        self.get_selected_columns()
        self.model.create_model(columns_selected=self.columns_selected,output_column=self.output_column, data_table_df=self.data_table_df)
        messagebox.showinfo("Model Created", "The model has been succesfully created.")

    def save_model(self):
        if self.model and self.model.model is not None:
            self.model.save_model()
        else:
            messagebox.showerror("Error", "No model has been created to save.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = GUI(root)
    root.mainloop()