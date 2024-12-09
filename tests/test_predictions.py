import pytest
from unittest.mock import Mock
from backend.predictions import Predictions

@pytest.fixture
def setup_predictions_logic():
    """Configuración básica para pruebas sin crear ventanas."""
    formula = {"formula": "y = [2.0] * ['x1'] + 5.0"}  # Ejemplo de fórmula simple
    root_mock = Mock()  # No usamos una ventana real
    result_prediction_label_mock = Mock()
    return Predictions(formula, root_mock, result_prediction_label_mock)

def test_calculate_prediction_missing_input_logic(setup_predictions_logic):
    """Prueba para asegurarse de que se maneje una entrada faltante."""
    predictions = setup_predictions_logic
    predictions.coefficients = [2.0]
    predictions.columns = ['x1']
    predictions.formula_intercept = 5.0
    
    # Simular valores de entrada faltantes
    predictions.column_vars = {'x1': Mock(get=lambda: "")}  # Simula un valor vacío
    
    with pytest.raises(ValueError, match="Please enter all values for the variables."):
        predictions.calculate_prediction()

def test_calculate_prediction_valid_input_logic(setup_predictions_logic):
    """Prueba para asegurarse de que se realice el cálculo de la predicción con entradas válidas."""
    predictions = setup_predictions_logic
    predictions.coefficients = [2.0] 
    predictions.columns = ['x1'] 
    predictions.formula_intercept = 5.0
    predictions.column_vars = {'x1': Mock(get=lambda: "3")} 
    predictions.result_var = Mock() 
    predictions.calculate_prediction()
    predictions.result_var.set.assert_called_with("11.0000")