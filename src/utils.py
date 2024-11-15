from tkinter import messagebox
from numpy import np

def validate_numeric_columns(data, columns):
    """Valida que las columnas seleccionadas sean numéricas."""
    for col in columns:
        if not np.issubdtype(data[col].dtype, np.number):
            return False
    return True

def show_message(title, message):
    """Muestra un mensaje en un cuadro de diálogo."""
    messagebox.showinfo(title, message)