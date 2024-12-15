from tkinter import Toplevel, StringVar, messagebox
import customtkinter as ctk
from unittest.mock import Mock


#======================================= PREDICTIONS ==================================

class Predictions:
    """Generates predictions based on a formula and user input."""

    def __init__(self, formula, root, result_prediction_label):
        """Initializes the Predictions class with a formula, root window, and result display.

        Args:
            formula (dict): Contains the formula used for prediction.
            root (Tk): Root Tkinter window.
            result_prediction_label (Widget): Label to display prediction results.
        """

        self.formula = formula
        self.root = root
        self.result_prediction_label = result_prediction_label

        if isinstance(root, Mock):
            self.result_var = Mock()  
        else:
            self.result_var = StringVar()

    #------------------------------ PREDCTIONS WINDOW ------------------------------

    def predictions(self):
        """Parses the formula and sets up a GUI for user input and predictions."""

        #------------------------ Get data ------------------------

        formula_sep = self.formula["formula"]
        
        coef_part = formula_sep.split('=')[1].split('*')[0].strip() 
        coef_str = coef_part.strip('[]')  # Elimina los corchetes
        self.coefficients = [float(x) for x in coef_str.split()]

        columns_part = formula_sep.split('*')[1].split('+')[0].strip()  
        columns_str = columns_part.strip("[]")  # Elimina los corchetes
        self.columns = [col.strip(" '") for col in columns_str.split(',')] 

        self.formula_intercept = float(formula_sep.split('+')[-1].strip())  

        #--------------- Create predictions window ----------------
        
        self.predictions_window = Toplevel(self.root)
        self.predictions_window.title("Predictions")
        self.predictions_window.resizable(False, False)
        self.predictions_window.configure(bg="#dfe6e9")

        title_frame = ctk.CTkFrame(
            self.predictions_window,
            fg_color="#2c3e50",  
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(10, 5), padx=0)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Prediction Values",
            text_color="#ecf0f1",  
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=5)

        options_frame = ctk.CTkFrame(
            self.predictions_window,
            fg_color="#f1f2f6",  
            corner_radius=10
        )
        options_frame.pack(pady=(5, 5), padx=10, fill="both", expand=True)

        self.column_vars = {}

        for col in self.columns:
            var = StringVar()  
            self.column_vars[col] = var

            col_label = ctk.CTkLabel(
                options_frame,
                text=col,
                text_color="#2c3e50",
                font=("Helvetica", 12)
            )
            col_label.pack(anchor="w", padx=10, pady=2)

            col_entry = ctk.CTkEntry(
                options_frame,
                textvariable=var,
                font=("Helvetica", 12)
            )
            col_entry.pack(fill="x", padx=10, pady=2)

        predicted_label = ctk.CTkLabel(
            options_frame,
            text="Predicted Value",
            text_color="#2c3e50",
            font=("Helvetica", 12)
        )
        predicted_label.pack(anchor="w", padx=10, pady=2)

        result_frame = ctk.CTkFrame(
            options_frame,
            fg_color="#bdc3c7",  
            corner_radius=10
        )
        result_frame.pack(fill="x", padx=10, pady=10)

        self.result_var = StringVar(value="")  
        self.result_entry = ctk.CTkEntry(
            result_frame,
            textvariable=self.result_var,
            font=("Helvetica", 14, "bold"),
            fg_color="#ecf0f1",  
            state="readonly",  
            text_color="#27ae60", 
            justify="center"  
        )
        self.result_entry.pack(fill="x", padx=5, pady=5)
        
        calculate_button = ctk.CTkButton(
            options_frame,
            text="Calculate Prediction",
            command=self.calculate_prediction,
            fg_color="#27ae60",  
            hover_color="#2ecc71"
        )
        calculate_button.pack(pady=10)

        close_button = ctk.CTkButton(
            options_frame,
            text="Close",
            command=self.predictions_window.destroy,
            fg_color="#e74c3c",  
            hover_color="#c0392b"
        )
        close_button.pack(pady=(5, 10))

    #------------------------------ CALCULATE PREDICTION ------------------------------

    def calculate_prediction(self):
        """Calculates the prediction based on user inputs and the provided formula."""

        values = [self.column_vars[col].get() for col in self.columns]
        

        self.validate_inputs(values)
        
        try:
            float_values = [float(v) for v in values]
            
            prediction = sum(coef * valor for coef, valor in zip(self.coefficients, float_values)) + self.formula_intercept                
            self.result_prediction_label.configure(text=f"Result: {prediction}")
            
            self.result_var.set(f"{prediction:.4f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def validate_inputs(self, values):
        """Validates user inputs before performing predictions.

        Args:
            values (list): List of user-provided input values.

        Raises:
            ValueError: If any input value is missing or invalid.
        """

        if any(v.strip() == "" for v in values): 
            messagebox.showerror("Error", "Enter all values for the variables.")
            raise ValueError("Please enter all values for the variables.")
