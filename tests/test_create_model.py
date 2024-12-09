import pytest
from unittest.mock import Mock, patch
from backend.model import Model
import pandas as pd

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

@patch("tkinter.Tk", Mock())  # Mock de la ventana principal
@patch("tkinter.messagebox.showinfo", Mock())  # Mock del messagebox
def test_create_model(setup_model):
    """Test that a model can be created successfully."""
    # Tu prueba sin la interfaz gráfica real
    data_table = pd.DataFrame({
        "x1": [1, 2, 3],
        "x2": [4, 5, 6],
        "y": [7, 8, 9]
    })
    setup_model.create_model(["x1", "x2"], "y", data_table, Mock(), Mock(), Mock())

    assert setup_model.model is not None, "Model was not created."
