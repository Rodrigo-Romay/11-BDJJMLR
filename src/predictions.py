from tkinter import Toplevel, IntVar, messagebox
import customtkinter as ctk


class Predictions:
    def __init__(self, formula, root):
        self.formula = formula
        self.root = root

    def predictions(self):
        # Separar la fórmula
        formula_sep = self.formula["formula"]
        
        # Extraer los coeficientes
        coef_part = formula_sep.split('=')[1].split('*')[0].strip()  # Toma la parte entre "=" y "*"
        coef_str = coef_part.strip('[]')  # Elimina los corchetes
        coefficients = [float(x) for x in coef_str.split()]
        # Extraer las columnas
        columns_part = formula_sep.split('*')[1].split('+')[0].strip()  # Toma la parte entre "*" y "+"
        columns_str = columns_part.strip("[]")  # Elimina los corchetes
        columns = [col.strip(" '") for col in columns_str.split(',')]  # Limpia y separa las columnas

        # Extraer el intercepto
        formula_intercept = float(formula_sep.split('+')[-1].strip())  # Intercepto final

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
        for col in columns:
            var = IntVar()  # Cambiar a DoubleVar() si necesitas decimales
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

        # Botón para calcular predicción
        def calcular_prediccion():
            try:
                # Recoger los valores introducidos
                valores = [self.column_vars[col].get() for col in columns]
                
                # Calcular la predicción: sum(coef * valor) + intercepto
                prediccion = sum(coef * valor for coef, valor in zip(coefficients, valores)) + formula_intercept
                
                # Mostrar predicción
                messagebox.showinfo("Prediction Result", f"The predicted value is: {prediccion:.4f}")

                self.predictions_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        calcular_button = ctk.CTkButton(
            options_frame,
            text="Calculate Prediction",
            command=calcular_prediccion,
            fg_color="#27ae60",  # Verde
            hover_color="#2ecc71"
        )
        calcular_button.pack(pady=10)

# Ejemplo de uso
if __name__ == "__main__":
    root = ctk.CTk()
    formula = {"formula": "median_income = [-2.28339800e-04 8.19880332e-05] * ['total_bedrooms', 'population'] + 3.8766"}
    app = Predictions(formula, root)
    app.predictions()
    root.mainloop()
