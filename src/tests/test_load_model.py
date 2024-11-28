import pytest
from unittest.mock import Mock, patch
from model_updated_interface2 import Model
import pickle

@pytest.fixture
def setup_model():
    save_button_mock = Mock()
    load_button_mock = Mock()
    return Model(save_button_mock, load_button_mock)

def test_load_valid_file(setup_model, tmpdir):
    model_data = {
        "formula": "y = 2x + 1",
        "description": "Test model",
        "metrics": {"mse": 0.02, "r2": 0.98},  # Encapsular mse y r2 en 'metrics'
        "input_columns": ["x"],
        "output_column": "y"
    }
    model_file = tmpdir.join("test_model.pkl")
    with open(model_file, "wb") as f:
        pickle.dump(model_data, f)

    # Mock para devolver path temporal
    with patch("tkinter.filedialog.askopenfilename", return_value=str(model_file)):
        setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    #Compara si son iguales los datos cargados
    assert setup_model.model_formula == model_data["formula"], "La fórmula no se cargó correctamente."
    assert setup_model.model_metrics["mse"] == model_data["metrics"]["mse"], "The MSE value was not loaded correctly."
    assert setup_model.model_metrics["r2"] == model_data["metrics"]["r2"], "The R2 value was not loaded correctly."

def test_load_model_invalid_file(setup_model):
    # Mock para devolver una ruta no existente
    with patch("tkinter.filedialog.askopenfilename", return_value="non_existent_model.pkl"):
        with pytest.raises(FileNotFoundError):
            setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())

def test_load_model_corrupted_file(setup_model, tmpdir):
    """Test that loading a corrupted model file raises a general error for both .pkl and .joblib."""

    # Crear un archivo .pkl corrupto
    corrupted_pkl_file = tmpdir.join("corrupted_model.pkl")
    with open(corrupted_pkl_file, "wb") as f:
        f.write(b"corrupted data")

    # Crear un archivo .joblib corrupto
    corrupted_joblib_file = tmpdir.join("corrupted_model.joblib")
    with open(corrupted_joblib_file, "wb") as f:
        f.write(b"corrupted data")

    # Mock para .pkl corrupto
    with patch("tkinter.filedialog.askopenfilename", return_value=str(corrupted_pkl_file)):
        with pytest.raises(Exception):  # Esperamos cualquier tipo de excepción para el archivo .pkl corrupto
            setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())

    # Mock para .joblib corrupto
    with patch("tkinter.filedialog.askopenfilename", return_value=str(corrupted_joblib_file)):
        with pytest.raises(Exception):  # Esperamos cualquier tipo de excepción para el archivo .joblib corrupto
            setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
