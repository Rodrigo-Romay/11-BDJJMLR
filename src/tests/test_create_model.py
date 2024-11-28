import pytest
from unittest.mock import Mock
from model_updated_interface2 import Model
import pandas as pd

@pytest.fixture
def setup_model():
    save_button_mock = Mock()
    load_button_mock = Mock()
    return Model(save_button_mock, load_button_mock)

def test_model_creation(setup_model):
    """Test that a model can be successfully created with given input and output columns."""
    # Mock data table with numerical values
    data = {
        "x1": [1, 2, 3, 4, 5],
        "x2": [2, 4, 6, 8, 10],
        "y": [1.5, 3.5, 5.5, 7.5, 9.5]
    }
    data_table_df = pd.DataFrame(data)

    # Setting up model parameters
    input_columns = ["x1", "x2"]
    output_column = "y"

    # Mock labels to display output
    formula_label_mock = Mock()
    mse_label_mock = Mock()
    r2_label_mock = Mock()

    # Create the model
    setup_model.create_model(input_columns, output_column, data_table_df, formula_label_mock, mse_label_mock, r2_label_mock)

    # Assertions
    assert setup_model.model is not None, "Model was not created successfully."
    assert setup_model.model_formula, "Model formula was not set."
    assert setup_model.model_metrics, "Model metrics were not set."