import pytest
from unittest.mock import Mock
from predictions import Predictions
from tkinter import Tk
import customtkinter as ctk

@pytest.fixture
def setup_predictions():
    root = Tk()  # Crear un root de tkinter para usar en la ventana de predicciones
    ctk.set_appearance_mode("light")
    formula = {"formula": "y = [2.0] * ['x1'] + 5.0"}  # Ejemplo de fórmula simple
    result_prediction_label_mock = Mock()
    return Predictions(formula, root, result_prediction_label_mock)

def test_calculate_prediction_valid_input(setup_predictions):
    """Test to ensure a valid prediction is calculated when inputs are correct."""
    setup_predictions.predictions()  # Crear la ventana y las entradas
    setup_predictions.column_vars['x1'].set("3")  # Asignar un valor numérico

    # Calcular la predicción y verificar el resultado
    setup_predictions.calculate_prediction()
    assert setup_predictions.result_var.get() != "", "Prediction value was not calculated correctly."

def test_calculate_prediction_missing_input(setup_predictions):
    """Test to ensure a ValueError is raised when input is missing."""
    setup_predictions.predictions()  # Crear la ventana y las entradas
    setup_predictions.column_vars['x1'].set("")  # Dejar el valor vacío

    with pytest.raises(ValueError, match="Please enter all values for the variables."):
        setup_predictions.calculate_prediction()

