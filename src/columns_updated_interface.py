import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, IntVar, simpledialog
from tkinter import ttk

class Columns():

    def __init__(self,root,data_table,input_columns_label,output_column_label, create_model_button):
        self.root = root
        self.data_table = data_table
        self.input_columns_label = input_columns_label
        self.output_column_label = output_column_label
        self.column_vars = {}
        self.columns_selected = []
        self.output_column = None
        self.create_model_button = create_model_button 


    def select_columns(self):
        self.column_window = Toplevel(self.root)
        self.column_window.title("Select Input Columns")
        self.column_vars = {}

        for col in self.data_table["columns"]:
            var = IntVar()
            self.column_vars[col] = var
            checkbox = ctk.CTkCheckBox(self.column_window, text=col, variable=var)
            checkbox.pack(anchor="w")

        confirm_button = ctk.CTkButton(self.column_window, text="Confirm", command=lambda: self.confirm_columns(self.column_window))
        confirm_button.pack(pady=10)

    def confirm_columns(self, window):
        self.columns_selected = [col for col, var in self.column_vars.items() if var.get() == 1]
        if self.columns_selected:
            self.input_columns_label.configure(text=f"Features: {', '.join(self.columns_selected)}")
        self.column_window.destroy()

    def select_output_column(self):
        self.output_window = Toplevel(self.root)
        self.output_window.title("Select Output Column")
        self.output_var = ctk.StringVar()

        for col in self.data_table["columns"]:
            radio = ctk.CTkRadioButton(self.output_window, text=col, variable=self.output_var, value=col)
            radio.pack(anchor="w")

        confirm_button = ctk.CTkButton(self.output_window, text="Confirm", command=lambda: self.confirm_output_column(self.output_window))
        confirm_button.pack(pady=10)

    def confirm_output_column(self, window):
        self.output_column = self.output_var.get()
        if self.output_column:
            self.output_column_label.configure(text=f"Target: {self.output_column}")
            self.create_model_button.configure(state="normal")
        self.output_window.destroy()

  
