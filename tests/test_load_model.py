import pytest
from unittest.mock import Mock, MagicMock, patch
from backend.model import Model
import pickle

@pytest.fixture
def setup_model():
    save_button_mock = Mock()
    load_button_mock = Mock()
    predict_button_mock = Mock()
    show_model_button_mock = Mock()
    preprocess_button_mock = Mock()
    select_columns_button_mock = Mock()
    select_output_button_mock = Mock()
    null_option_menu_mock = Mock()
    create_model_button_mock = Mock()
    constant_entry_mock = Mock()
    null_handling_label_mock = Mock()
    null_handling_frame_mock = Mock()

    return Model(
        save_button_mock, 
        load_button_mock, 
        predict_button_mock, 
        show_model_button_mock, 
        preprocess_button_mock, 
        select_columns_button_mock, 
        select_output_button_mock, 
        null_option_menu_mock, 
        create_model_button_mock,
        constant_entry_mock,
        null_handling_label_mock,
        null_handling_frame_mock,
        load_button_mock
    )

def test_load_valid_file(setup_model, tmpdir):
    model_data = {
        "formula": "y = 2x + 1",
        "description": "Test model",
        "metrics": {"mse": 0.02, "r2": 0.98},
        "input_columns": ["x"],
        "output_column": "y"
    }
    model_file = tmpdir.join("test_model.pkl")
    with open(model_file, "wb") as f:
        pickle.dump(model_data, f)

    with patch("tkinter.filedialog.askopenfilename", return_value=str(model_file)), \
         patch("tkinter.messagebox.showinfo") as mock_showinfo:

        result_prediction_label_mock = Mock()
        file_path_label_mock = Mock()
        data_table_mock = MagicMock()
        data_table_mock.get_children.return_value = ["item1", "item2"]

        setup_model.load_model(
            Mock(),  # input_columns_label
            Mock(),  # output_column_label
            Mock(),  # formula_label
            Mock(),  # load_description_label
            Mock(),  # mse_label
            Mock(),  # r2_label
            result_prediction_label_mock,
            file_path_label_mock,
            data_table_mock
        )
        mock_showinfo.assert_called_once_with("Model Loaded", "Model loaded successfully.")

    # Compara si son iguales los datos cargados
    assert setup_model.model_formula == model_data["formula"], "La fórmula no se cargó correctamente."
    assert setup_model.model_metrics["mse"] == model_data["metrics"]["mse"], "El valor de MSE no se cargó correctamente."
    assert setup_model.model_metrics["r2"] == model_data["metrics"]["r2"], "El valor de R2 no se cargó correctamente."

def test_load_model_invalid_file(setup_model):
    # Mock para devolver una ruta no existente
    with patch("tkinter.filedialog.askopenfilename", return_value="non_existent_model.pkl"):
        with pytest.raises(FileNotFoundError):
            setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(),Mock(), Mock(), Mock())

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
            setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(),Mock(), Mock(), Mock())

    # Mock para .joblib corrupto
    with patch("tkinter.filedialog.askopenfilename", return_value=str(corrupted_joblib_file)):
        with pytest.raises(Exception):  # Esperamos cualquier tipo de excepción para el archivo .joblib corrupto
            setup_model.load_model(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(),Mock(), Mock(), Mock())
