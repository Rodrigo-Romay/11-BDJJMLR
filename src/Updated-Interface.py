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
        self.model = None  # Para almacenar el modelo creado

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.geometry("1200x800")
        self.root.configure(bg="white")

        self.title_label = ctk.CTkLabel(self.root, text="Preprocessing Dataset", font=("Roboto", 24, "bold"), text_color="black")
        self.title_label.pack(pady=10)

        self.load_button = ctk.CTkButton(self.root, text="OPEN FILE", command=self.load_file, corner_radius=8,
                                         fg_color="#ffcc00", hover_color="#ffb700", text_color="black", font=("Roboto", 14, "bold"))
        self.load_button.pack(pady=10)

        self.file_label = ctk.CTkLabel(self.root, text="", font=("Roboto", 12), text_color="gray")
        self.file_label.pack()

        self.table_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="white")
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.data_table = ttk.Treeview(self.table_frame, show="headings")
        self.data_table.pack(expand=True, fill="both")

        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 12), background="white", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", font=("Roboto", 14, "bold"), background="#e6e6e6", foreground="black")

        self.features_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.features_frame.pack(pady=5, fill="x")

        self.input_columns_label = ctk.CTkLabel(self.features_frame, text="Features: None", font=("Roboto", 14), text_color="black")
        self.input_columns_label.pack(side="left", padx=(20, 5))

        self.output_column_label = ctk.CTkLabel(self.features_frame, text="Target: None", font=("Roboto", 14), text_color="black")
        self.output_column_label.pack(side="left", padx=5)

        self.preprocess_button = ctk.CTkButton(self.root, text="Preprocess Data", command=self.preprocess_data, corner_radius=8,
                                               fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.preprocess_button.pack(pady=10)
        self.preprocess_button.configure(state="disabled")

        self.null_option_label = ctk.CTkLabel(self.root, text="Handle Null Values:", font=("Roboto", 14), text_color="black")
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

        self.select_columns_button = ctk.CTkButton(self.root, text="Select Input Columns", command=self.select_columns, corner_radius=8,
                                                   fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.select_columns_button.pack(pady=10)
        self.select_columns_button.configure(state="disabled")

        self.select_output_button = ctk.CTkButton(self.root, text="Select Output Column", command=self.select_output_column, corner_radius=8,
                                                  fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.select_output_button.pack(pady=10)
        self.select_output_button.configure(state="disabled")

        self.create_model_button = ctk.CTkButton(self.root, text="Create Model", command=self.create_model, corner_radius=8,
                                                 fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.create_model_button.pack(pady=10)
        self.create_model_button.configure(state="disabled")

        self.save_button = ctk.CTkButton(self.root, text="Save Model", command=self.save_model, corner_radius=8,
                                         fg_color="#0078d7", hover_color="#005a9e", text_color="white")
        self.save_button.pack(pady=10)
        self.save_button.configure(state="disabled")

        self.description_label = ctk.CTkLabel(self.root, text="Model Description:", font=("Roboto", 14), text_color="black")
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

    def select_columns(self):
        column_window = Toplevel(self.root)
        column_window.title("Select Input Columns")
        self.column_vars = {}

        for col in self.data_table["columns"]:
            var = IntVar()
            self.column_vars[col] = var
            checkbox = ctk.CTkCheckBox(column_window, text=col, variable=var)
            checkbox.pack(anchor="w")

        confirm_button = ctk.CTkButton(column_window, text="Confirm", command=lambda: self.confirm_columns(column_window))
        confirm_button.pack(pady=10)

    def confirm_columns(self, window):
        self.columns_selected = [col for col, var in self.column_vars.items() if var.get() == 1]
        if self.columns_selected:
            self.input_columns_label.configure(text=f"Features: {', '.join(self.columns_selected)}")
        window.destroy()

    def select_output_column(self):
        output_window = Toplevel(self.root)
        output_window.title("Select Output Column")
        self.output_var = ctk.StringVar()

        for col in self.data_table["columns"]:
            radio = ctk.CTkRadioButton(output_window, text=col, variable=self.output_var, value=col)
            radio.pack(anchor="w")

        confirm_button = ctk.CTkButton(output_window, text="Confirm", command=lambda: self.confirm_output_column(output_window))
        confirm_button.pack(pady=10)

    def confirm_output_column(self, window):
        self.output_column = self.output_var.get()
        if self.output_column:
            self.output_column_label.configure(text=f"Target: {self.output_column}")
            self.create_model_button.configure(state="normal")
        window.destroy()

    def save_description(self):
        self.description_saved = self.description_entry.get()
        if self.description_saved:
            messagebox.showinfo("Success", "Description saved successfully!")
        else:
            messagebox.showwarning("Warning", "Description is empty. Please enter a description.")

    def create_model(self):
        if not self.columns_selected or not self.output_column:
            messagebox.showerror("Error", "Please select input and output columns.")
            return

        try:
            X = self.data_table_df[self.columns_selected].values
            y = self.data_table_df[self.output_column].values
            if not (np.issubdtype(X.dtype, np.number) and np.issubdtype(y.dtype, np.number)):
                raise ValueError("Columns must contain numeric values.")

            self.model = LinearRegression()
            self.model.fit(X, y)
            y_pred = self.model.predict(X)
            r2 = self.model.score(X, y)
            mse = mean_squared_error(y, y_pred)
            self.model_formula = {"formula": f"{self.output_column} = {self.model.coef_} * {self.columns_selected} + {self.model.intercept_}"}
            self.model_metrics = {"r2": r2, "mse": mse}

            messagebox.showinfo("Model Created", f"RÂ²: {r2:.4f}\nMSE: {mse:.4f}")

            if X.shape[1] == 1:
                self.plot_model_2d(X, y, y_pred, r2, mse)
            elif X.shape[1] == 2:
                self.plot_model_3d(X, y, y_pred, r2, mse)
            else:
                messagebox.showinfo("Model Created", "Model created successfully, but cannot plot with more than 2 features.")
            self.save_button.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Model Error", f"An error occurred: {e}")

    def plot_model_2d(self, X, y, y_pred, r2, mse):
        plt.figure(figsize=(10, 6))
        plt.scatter(X, y, color="blue", label="Actual Data")
        plt.plot(X, y_pred, color="red", label="Predicted Line")
        plt.xlabel(self.columns_selected[0])
        plt.ylabel(self.output_column)
        plt.title("Linear Regression Model (2D)")
        plt.legend()
        plt.suptitle(f"{self.output_column} = {self.model_formula['formula']}\nRÂ² = {r2:.4f}, ECM = {mse:.4f}", fontsize=10, color="black")
        plt.show()

    def plot_model_3d(self, X, y, y_pred, r2, mse):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(X[:, 0], X[:, 1], y, color="blue", label="Actual Data")
        ax.plot_trisurf(X[:, 0], X[:, 1], y_pred, color="red", alpha=0.6)
        ax.set_xlabel(self.columns_selected[0])
        ax.set_ylabel(self.columns_selected[1])
        ax.set_zlabel(self.output_column)
        ax.set_title("Linear Regression Model (3D)")
        plt.suptitle(f"{self.output_column} = {self.model_formula['formula']}\nRÂ² = {r2:.4f}, ECM = {mse:.4f}", fontsize=10, color="black")
        plt.legend()
        plt.show()

    def save_model(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")])
        if file_path:
            try:
                model_data = {
                    "model": self.model,  # Guardar el modelo
                    "formula": self.model_formula,
                    "input_columns": self.columns_selected,
                    "output_column": self.output_column,
                    "metrics": self.model_metrics,
                    "description": self.description_saved
                }
                if file_path.endswith(".pkl"):
                    with open(file_path, "wb") as file:
                        pickle.dump(model_data, file)
                elif file_path.endswith(".joblib"):
                    joblib.dump(model_data, file_path)
                messagebox.showinfo("Model Saved", f"Model saved at {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving model: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = GUI(root)
    root.mainloop()