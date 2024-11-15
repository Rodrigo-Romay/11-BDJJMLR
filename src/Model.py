import numpy as np
import pickle
import joblib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from tkinter import messagebox, filedialog

class Model:
    def __init__(self):
        self.model_formula = {}
        self.model_metrics = {}
        self.description_saved = {}
        self.columns_selected = None
        self.output_column = None
        self.data_table_df = None
        self.model = None

    def create_model(self, columns_selected, output_column, data_table_df):
        self.columns_selected = columns_selected
        self.output_column = output_column
        self.data_table_df = data_table_df

        if self.columns_selected and self.output_column and not self.data_table_df.empty:
            try:
                X = self.data_table_df[self.columns_selected].values
                y = self.data_table_df[self.output_column].values  
                if not self.description_saved:
                    messagebox.showinfo("Reminder", "No description saved.")
                if np.issubdtype(X.dtype, np.number) and np.issubdtype(y.dtype, np.number):
                    model = LinearRegression()
                    model.fit(X, y)
                    if X.shape[1] == 1:  
                        self.graphic_2D(X, y, model)
                    elif X.shape[1] == 2:  
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
        file_path = filedialog.asksaveasfilename(filetypes=[("PKL files", "*.pkl"), ("Joblib files", "*.joblib")])
        if file_path:
            try:
                model_data = {
                    "formula": self.model_formula,
                    "input_columns": self.columns_selected,
                    "output_column": self.output_column,
                    "r2_score": self.model_metrics.get("r2"),
                    "ecm": self.model_metrics.get("ecm"),
                    "description" : self.description_saved
                    }
                if file_path.endswith(".pkl"):
                    with open(file_path, 'wb') as file:
                        pickle.dump(model_data, file)
                elif file_path.endswith(".joblib"):
                    joblib.dump(model_data, file_path)
                else:
                    raise ValueError("Unsupported file format.")
                messagebox.showinfo("Model saved", f"Model saved successfully from {file_path}.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the model: {str(e)}")
    
    def graphic_2D(self, X, y, model):
        fig, ax = plt.subplots(figsize=(8, 6))    
        ax.scatter(X, y, color='blue', label='Data')
        ax.plot(X, model.predict(X), color='red', label='Regression Line')
        ax.set_xlabel(f"Input: {self.columns_selected[0]}", labelpad=15, color='black', fontsize=18)
        ax.set_ylabel(f"Output: {self.output_column}", labelpad=15, color='black', fontsize=18)
        ax.set_title('Linear Regression')
        coef = model.coef_[0]
        intercept = model.intercept_
        formula_str = f"{self.output_column} = {coef:.2f} * {self.columns_selected[0]} + {intercept:.2f}"
        y_pred = model.predict(X)
        r2_score = model.score(X, y)  
        ecm = np.mean((y - y_pred) ** 2)  
        self.model_formula = {"formula":formula_str}
        self.model_metrics = {"r2": r2_score, "ecm":ecm}
        r2_str = f"R² = {r2_score:.4f}"
        mse_str = f"ECM = {ecm:.4f}"
        fig.text(0.90, 0.97, r2_str, ha='left', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))
        fig.text(0.90, 0.94, mse_str, ha='left', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))
        plt.suptitle(formula_str, fontsize=12, color='black', ha='center', bbox=dict(facecolor='white', alpha=0.5))
        ax.legend()
        plt.show()

    def graphic_3D(self, X, y, model):
        try:
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(X[:, 0], X[:, 1], y, color='b', label='Data')
            y_pred = model.predict(X)
            ax.plot_trisurf(X[:, 0], X[:, 1], y_pred, color='red', alpha=0.5, label='Regression Model')
            ax.set_xlabel(self.columns_selected[0], labelpad=10, color='black')
            ax.set_ylabel(self.columns_selected[1], labelpad=10, color='black')
            ax.set_zlabel(self.output_column, labelpad=10, color='black')
            formula_str = f"{self.output_column} = {model.coef_[0]:.2f} * {self.columns_selected[0]} + {model.coef_[1]:.2f} * {self.columns_selected[1]} + {model.intercept_:.2f}"
            r2_score = model.score(X, y)
            r2_str = f"R² = {r2_score:.4f}"
            ecm = mean_squared_error(y, y_pred)
            ecm_str = f"ECM = {ecm:.4f}"
            self.model_formula = {"formula":formula_str}
            self.model_metrics = {"r2":r2_score, "ecm": ecm}
            plt.suptitle(formula_str, fontsize=12, color='black', ha='center', bbox=dict(facecolor='white', alpha=0.7))
            fig.text(0.90, 0.97, r2_str, ha='left', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))
            fig.text(0.90, 0.94, ecm_str, ha='left', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))
            fig.patch.set_facecolor('white')        
            ax.set_facecolor('whitesmoke')          
            ax.grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
            ax.view_init(elev=30, azim=45)
            ax.tick_params(axis='both', colors='black', direction='in', length=5, width=1)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting 3D data: {str(e)}")

    def model_description(self, description):
        self.description_saved = {"description": description}