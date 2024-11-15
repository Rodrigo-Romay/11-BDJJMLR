import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, IntVar, simpledialog
import numpy as np
import matplotlib.pyplot as plt


class Preprocess():
    def __init__(self,data_table_df,null_option_menu,display_data,constant_entry):
        self.data_table_df = data_table_df
        self.null_option_menu = null_option_menu
        self.display_data = display_data
        self.constant_entry = constant_entry
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
                
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for the constant.")