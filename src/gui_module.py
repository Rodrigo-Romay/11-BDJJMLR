import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk, Toplevel, IntVar, StringVar
import numpy as np
from Model import Model
from Modulo import DataImport
from columns import Columns
from preprocess_updated_interface2 import Preprocess

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trendify")
        self.columns_selected = []
        self.output_column = None 
        self.description_saved = {}
        self.model = Model()
        self.data_table_df = None
        self.create_widgets()

    def create_widgets(self):
        self.create_title_label()
        self.create_file_controls()
        self.create_outer_frame()
        self.create_data_table()
        self.create_preprocess_controls()
        self.create_column_selection_controls()
        self.create_model_controls()
        self.create_description_widgets()

    def create_title_label(self):
        title_label = ctk.CTkLabel(self.root, text="Trendify", font=("Pacifico", 50, "bold"), text_color="#d1d9e6")
        title_label.place(relx=0.5, y=20, anchor="n")

    def create_file_controls(self):
        load_button = ctk.CTkButton(self.root, text="Load File", command=self.load_file)
        load_button.place(relx=0.5, y=100, anchor="n")

        self.file_label = ctk.CTkLabel(self.root, text="File's Route:")
        self.file_label.place(relx=0.5, y=140, anchor="n")

    def create_outer_frame(self):
        self.outer_frame = ctk.CTkFrame(self.root)
        self.outer_frame.place(relx=0.5, rely=0.25, anchor="n", relwidth=0.9, relheight=0.3)

    def create_data_table(self):
        self.table_frame = ctk.CTkFrame(self.outer_frame)
        self.table_frame.pack(padx=15, pady=15, fill="both", expand=True)
        
        self.data_table = self.create_treeview()
        self.create_scrollbars()

    def create_treeview(self):
        data_table = ttk.Treeview(self.table_frame, show="headings")
        data_table.pack(expand=True, fill="both")
        return data_table

    def create_scrollbars(self):
        self.v_scroll = ctk.CTkScrollbar(self.table_frame, orientation="vertical", command=self.data_table.yview)
        self.h_scroll = ctk.CTkScrollbar(self.table_frame, orientation="horizontal", command=self.data_table.xview)
        self.data_table.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

    def create_preprocess_controls(self):
        self.null_handling_option = StringVar(value="Select an option")
        self.null_option_menu = ctk.CTkOptionMenu(
            self.root,
            variable=self.null_handling_option,
            values=["Delete rows with nulls", "Fill with mean", "Fill with median", "Fill with constant"]
        )
        self.null_option_menu.place(relx=0.25, rely=0.65, anchor="center")

        self.constant_entry = ctk.CTkEntry(self.root, placeholder_text="Constant")
        self.constant_entry.place(relx=0.25, rely=0.7, anchor="center")

        self.preprocess_button = ctk.CTkButton(self.root, text="Preprocess Data", command=self.preprocess)
        self.preprocess_button.place(relx=0.25, rely=0.75, anchor="center")

    def create_column_selection_controls(self):
        self.select_columns_button = ctk.CTkButton(self.root, text="Select Input Columns", command=self.select_columns)
        self.select_columns_button.place(relx=0.75, rely=0.65, anchor="center")

        self.select_output_button = ctk.CTkButton(self.root, text="Select Output Column", command=self.output_columns)
        self.select_output_button.place(relx=0.75, rely=0.7, anchor="center")

        self.labels_frame = ctk.CTkFrame(self.root)
        self.labels_frame.place(relx=0.5, rely=0.85, anchor="center")

        self.input_columns_label = ctk.CTkLabel(self.labels_frame, text="Input Columns: None", font=("Roboto", 16), text_color="#A0A0A0")
        self.input_columns_label.pack(side="top", padx=(10, 0))
    
        self.output_column_label = ctk.CTkLabel(self.labels_frame, text="Output Column: None", font=("Roboto", 16), text_color="#A0A0A0")
        self.output_column_label.pack(side="bottom", padx=(10, 0))

    def create_model_controls(self):
        self.create_model_button = ctk.CTkButton(self.root, text="Create Model", command=self.create_model)
        self.create_model_button.place(relx=0.25, rely=0.85, anchor="center")

        self.save_model_button = ctk.CTkButton(self.root, text="Save Model", command=self.save_model)
        self.save_model_button.place(relx=0.75, rely=0.85, anchor="center")

    def create_description_widgets(self):
        self.description_text = ctk.CTkTextbox(self.root, width=300, height=100)
        self.description_text.place(relx=0.5, rely=0.95, anchor="center")

        self.save_description_button = ctk.CTkButton(self.root, text="Save Description", command=self.model_description)
        self.save_description_button.place(relx=0.5, rely=0.975, anchor="center")

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("SQLite Files", "*.db *.sqlite")]
        )
        if file_path:
            self._file = file_path
            self.file_label.configure(text=f"File's Route: {self._file}")
            self.import_data()

    def import_data(self):
        try:
            data_importer = DataImport(self._file)
            data_importer.file_type()  
            data = data_importer._data 
            if not data.empty:
                self.data_table_df = data
                self.display_data(data)
            else:
                self.handle_empty_data()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {str(e)}")

    def display_data(self, data):
        self.data_table.delete(*self.data_table.get_children())
        self.data_table["columns"] = list(data.columns)
        for col in data.columns:
            self.data_table.heading(col, text=col, anchor="center")
            self.data_table.column(col, anchor="center")
        for index, row in data.iterrows():
            self.data_table.insert("", "end", values=list(row))

    def handle_null_option(self,option):
        self.preprocess_data.handle_null_option(option)

    def preprocess(self):
        self.preprocess_data = Preprocess(self.data_table_df,self.null_option_menu,self.display_data,self.constant_entry)
        self.preprocess_data.preprocess_data()
    def hide_constant_entry(self):
        self.preprocess_data.hide_constant_entry()
    def apply_constant_fill(self):
        self.preprocess_data.apply_constant_fill()


    def select_columns(self):
        self.select_columns_input = Columns(self.root,self.data_table,self.input_columns_label,self.output_column_label)
        self.select_columns_input.select_columns()
     

    def output_columns(self):
        self.select_output_column = Columns(self.root,self.data_table,self.input_columns_label,self.output_column_label)
        self.select_output_column.select_output_column()
    
    def get_selected_columns(self):
        self.columns_selected =  self.select_columns_input.columns_selected
        self.output_column =  self.select_output_column.output_column

    def create_model(self):
        self.get_selected_columns()
        self.model.create_model(columns_selected=self.columns_selected,output_column=self.output_column, data_table_df=self.data_table_df)
        messagebox.showinfo("Model Created", "The model has been succesfully created.")
    def save_model(self):
        if self.model and self.model.model is not None:
            self.model.save_model()
        else:
            messagebox.showerror("Error", "No model has been created to save.")

    def model_description(self):
        description = self.description_text.get("1.0", "end-1c")
        if not description:
            messagebox.showerror("Error", "Description is blank.")
        else:
            if self.model:
                self.model.model_description(description)
                messagebox.showinfo("Success", "Description saved successfully.")
            else:
                messagebox.showerror("Error", "No model")