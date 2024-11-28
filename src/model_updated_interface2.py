import numpy as np
import pickle
import joblib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from tkinter import messagebox, filedialog


class Model:
    def __init__(self, save_button, load_model_button):
        self.model_formula = {}
        self.model_metrics = {}
        self.description_saved = {}
        self.columns_selected = None
        self.output_column = None
        self.data_table_df = None
        self.model = None
        self.save_button = save_button
        self.load_model_button = load_model_button


    def create_model(self, columns_selected, output_column, data_table_df,formula_label, mse_label, r2_label):
        self.columns_selected = columns_selected
        self.output_column = output_column
        self.data_table_df = data_table_df
        if not self.description_saved:
            messagebox.showinfo("Reminder", "No description saved.")

        if not self.columns_selected or not self.output_column:
            messagebox.showerror("Error", "Please select input and output columns.")
            return

        try:
            X = self.data_table_df[self.columns_selected].values
            y = self.data_table_df[self.output_column].values
            if not (np.issubdtype(X.dtype, np.number) and np.issubdtype(y.dtype, np.number)):
                formula_label.configure(text="Formula: None")
                mse_label.configure(text="MSE: None")
                r2_label.configure(text="R2: None")
                raise ValueError("Columns must contain numeric values.")

            self.model = LinearRegression()
            self.model.fit(X, y)
            y_pred = self.model.predict(X)
            r2 = self.model.score(X, y)
            mse = mean_squared_error(y, y_pred)
            self.model_formula = {"formula": f"{self.output_column} = {self.model.coef_} * {self.columns_selected} + {self.model.intercept_:.4f}"}
            self.model_metrics = {"r2": r2, "mse": mse}

            formula=f"{self.output_column} = {self.model.coef_} * {self.columns_selected} + {self.model.intercept_:.4f}"
            formula_label.configure(text=f"Formula: {formula}")
            mse_label.configure(text=f"MSE: {mse:.4f}")
            r2_label.configure(text=f"R2: {r2:.4f}")

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
        plt.legend(loc='upper right')
        plt.suptitle(f"{self.output_column} = {self.model_formula['formula']}\nRÂ² = {r2:.4f}, MSE = {mse:.4f}", fontsize=10, color="black")
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
        plt.suptitle(f"{self.output_column} = {self.model_formula['formula']}\nRÂ² = {r2:.4f}, MSE = {mse:.4f}", fontsize=10, color="black")
        plt.legend(loc='upper right')
        plt.show()

    def save_model(self):
        file_path = filedialog.asksaveasfilename(
            filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")])
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

    def load_model(self,input_columns_label,output_column_label,formula_label,load_description_label,mse_label,r2_label):
        file_path = filedialog.askopenfilename(
            title="Select Model File",
            filetypes=[("PFL files", "*.pkl"), ("Joblib files", "*.joblib")]
        )
        if file_path:
            try:
                if file_path.endswith(".pkl"):
                    with open(file_path, 'rb') as file:
                        model_data = pickle.load(file)
                elif file_path.endswith(".joblib"):
                    model_data = joblib.load(file_path)
                else:
                    raise ValueError("Unsupported file format.")

                self.model = model_data.get("model")
                self.model_formula = model_data.get("formula")
                self.columns_selected = model_data.get("input_columns")
                self.output_column = model_data.get("output_column")
                self.model_metrics = model_data.get("metrics")
                self.description_saved = model_data.get("description", None)

                formula = self.model_formula.get("formula", "Formula not found")
                r2 = self.model_metrics.get("r2", "N/A")
                mse = self.model_metrics.get("mse", "N/A")
                description = self.description_saved or "No description saved."
                
                input_columns_label.configure(text=f"Input Columns: {', '.join(model_data['input_columns'])}")
                output_column_label.configure(text=f"Output Column: {model_data['output_column']}")
                formula_label.configure(text=f"Formula: {formula}")
                load_description_label.configure(text=f"Description: {description}")
                mse_label.configure(text=f"MSE: {mse:.4f}")
                r2_label.configure(text=f"R2: {r2:.4f}")
                
                messagebox.showinfo("Model Loaded", "Model loaded succesfully.")
            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading the model: {str(e)}")

    def save_description(self, description_saved):
        self.description_saved = description_saved
        if self.description_saved:
            messagebox.showinfo("Success", "Description saved successfully!")
        else:
            messagebox.showwarning("Warning", "Description is empty. Please enter a description.")