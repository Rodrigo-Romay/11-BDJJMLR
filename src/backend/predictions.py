from tkinter import Toplevel, StringVar, messagebox
import customtkinter as ctk


class Predictions:
    def __init__(self, formula, root, result_prediction_label):
        self.formula = formula
        self.root = root
        self.result_prediction_label = result_prediction_label

    def predictions(self):
        # Separar la fórmula
        formula_sep = self.formula["formula"]
        
        # Extraer los coeficientes
        coef_part = formula_sep.split('=')[1].split('*')[0].strip()  # Toma la parte entre "=" y "*"
        coef_str = coef_part.strip('[]')  # Elimina los corchetes
        self.coefficients = [float(x) for x in coef_str.split()]
        # Extraer las columnas
        columns_part = formula_sep.split('*')[1].split('+')[0].strip()  # Toma la parte entre "*" y "+"
        columns_str = columns_part.strip("[]")  # Elimina los corchetes
        self.columns = [col.strip(" '") for col in columns_str.split(',')]  # Limpia y separa las columnas

        # Extraer el intercepto
        self.formula_intercept = float(formula_sep.split('+')[-1].strip())  # Intercepto final

        # Crear ventana de predicciones
        self.predictions_window = Toplevel(self.root)
        self.predictions_window.title("Predictions")
        self.predictions_window.resizable(False, False)
        self.predictions_window.configure(bg="#dfe6e9")

        # Título
        title_frame = ctk.CTkFrame(
            self.predictions_window,
            fg_color="#2c3e50",  # Azul oscuro
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(10, 5), padx=0)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Prediction Values",
            text_color="#ecf0f1",  # Texto claro
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=5)

        # Frame de opciones
        options_frame = ctk.CTkFrame(
            self.predictions_window,
            fg_color="#f1f2f6",  # Azul claro pálido
            corner_radius=10
        )
        options_frame.pack(pady=(5, 5), padx=10, fill="both", expand=True)

        # Variables para almacenar valores de entrada
        self.column_vars = {}

        # Crear entradas dinámicamente para cada columna
        for col in self.columns:
            var = StringVar()  # Cambiar a DoubleVar() si necesitas decimales
            self.column_vars[col] = var

            # Etiqueta para el nombre de la columna
            col_label = ctk.CTkLabel(
                options_frame,
                text=col,
                text_color="#2c3e50",
                font=("Helvetica", 12)
            )
            col_label.pack(anchor="w", padx=10, pady=2)

            # Campo de entrada para la columna
            col_entry = ctk.CTkEntry(
                options_frame,
                textvariable=var,
                font=("Helvetica", 12)
            )
            col_entry.pack(fill="x", padx=10, pady=2)

        # Etiqueta para el título "Predicted Value"
        predicted_label = ctk.CTkLabel(
            options_frame,
            text="Predicted Value",
            text_color="#2c3e50",
            font=("Helvetica", 12)
        )
        predicted_label.pack(anchor="w", padx=10, pady=2)

        # Frame para resaltar la casilla del resultado
        result_frame = ctk.CTkFrame(
            options_frame,
            fg_color="#bdc3c7",  # Color gris oscuro para el marco
            corner_radius=10
        )
        result_frame.pack(fill="x", padx=10, pady=10)

        # Campo de entrada para mostrar el resultado
        self.result_var = StringVar(value="")  # Texto inicial es "None"
        self.result_entry = ctk.CTkEntry(
            result_frame,
            textvariable=self.result_var,
            font=("Helvetica", 14, "bold"),
            fg_color="#ecf0f1",  # Fondo claro para el campo de entrada
            state="readonly",  # Modo de solo lectura
            text_color="#27ae60",  # Texto en verde
            justify="center"  # Centrar el texto dentro del campo
        )
        self.result_entry.pack(fill="x", padx=5, pady=5)
        
        calculate_button = ctk.CTkButton(
            options_frame,
            text="Calculate Prediction",
            command=self.calculate_prediction,
            fg_color="#27ae60",  # Verde
            hover_color="#2ecc71"
        )
        calculate_button.pack(pady=10)

        # Botón para cerrar la ventana de predicciones
        close_button = ctk.CTkButton(
            options_frame,
            text="Close",
            command=self.predictions_window.destroy,
            fg_color="#e74c3c",  # Rojo
            hover_color="#c0392b"
        )
        close_button.pack(pady=(5, 10))


        # Botón para calcular predicción
    def calculate_prediction(self):
        # Recoger los valores introducidos
        values = [self.column_vars[col].get() for col in self.columns]
        
        # Validar los valores ingresados
        self.validate_inputs(values)

        try:
            # Convertir a float los valores válidos
            float_values = [float(v) for v in values]
            
            # Calcular la predicción: sum(coef * valor) + intercepto
            prediction = sum(coef * valor for coef, valor in zip(self.coefficients, float_values)) + self.formula_intercept                
            self.result_prediction_label.configure(text=f"Result: {prediction}")
            
            # Mostrar predicción en el campo de entrada
            self.result_var.set(f"{prediction:.4f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def validate_inputs(self, values):
        # Comprobar si falta algún valor de entrada
        if any(v.strip() == "" for v in values):  # Verificar si algún valor está vacío
            raise ValueError("Please enter all values for the variables.")
