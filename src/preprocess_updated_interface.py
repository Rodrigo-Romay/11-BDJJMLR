import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, IntVar, simpledialog
import numpy as np
import matplotlib.pyplot as plt


class Preprocess():
    def __init__(self,data_table_df,null_option_menu,display_data,constant_entry, preprocess_button):
        self.data_table_df = data_table_df
        self.null_option_menu = null_option_menu
        self.display_data = display_data
        self.constant_entry = constant_entry
        self.preprocess_button = preprocess_button


    def preprocess_data(self):
        if self.data_table_df is not None:
            null_counts = self.data_table_df.isnull().sum()
            null_columns = null_counts[null_counts > 0].to_dict()
            if null_columns:
                messagebox.showinfo("Null Values Detected", f"Columns with null values:\n{null_columns}")
                self.null_option_menu.configure(state="normal")
            else:
                messagebox.showinfo("No Null Values", "No null values detected.")
            self.preprocess_button.configure(state="disabled")
        else:
            messagebox.showwarning("No Data", "Please load data first.")

    def handle_null_option(self, option):
        if option == "Delete rows with nulls":
            self.data_table_df.dropna(inplace=True)
            self.display_data(self.data_table_df)
            messagebox.showinfo("Success", "Rows with null values have been deleted.")
        elif option == "Fill with mean":
            for col in self.data_table_df.select_dtypes(include=[np.number]).columns:
                self.data_table_df[col].fillna(self.data_table_df[col].mean(), inplace=True)
            self.display_data(self.data_table_df)
            messagebox.showinfo("Success", "Null values have been filled with the mean.")
        elif option == "Fill with median":
            for col in self.data_table_df.select_dtypes(include=[np.number]).columns:
                self.data_table_df[col].fillna(self.data_table_df[col].median(), inplace=True)
            self.display_data(self.data_table_df)
            messagebox.showinfo("Success", "Null values have been filled with the median.")
        elif option == "Fill with constant":
            self.constant_entry.configure(state="normal")
            self.constant_entry.bind("<Return>", self.fill_with_constant)

    def fill_with_constant(self, event=None):
        try:
            constant_value = float(self.constant_entry.get())
            self.data_table_df.fillna(constant_value, inplace=True)
            self.display_data(self.data_table_df)
            messagebox.showinfo("Success", "Null values have been filled with the specified constant.")
            self.constant_entry.configure(state="disabled")
        except ValueError:
            messagebox.showerror("Error", "Invalid constant value. Please enter a numeric value.")
