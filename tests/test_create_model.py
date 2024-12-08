import pytest
from unittest.mock import Mock
from model_updated_interface2 import Model
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
    return Model(save_button_mock, load_button_mock, predict_button_mock, show_model_button_mock, preprocess_button_mock, select_columns_button_mock, select_output_button_mock, null_option_menu_mock, create_model_button_mock)

def test_create_model(setup_model):
    """Test that a model can be created successfully."""
    # Set up mock data for model creation
    data_table = pd.DataFrame({
        "x1": [1, 2, 3],
        "x2": [4, 5, 6],
        "y": [7, 8, 9]
    })
    setup_model.create_model(["x1", "x2"], "y", data_table, Mock(), Mock(), Mock())

    assert setup_model.model is not None, "Model was not created."
