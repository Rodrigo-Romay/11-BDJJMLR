import pytest
from unittest.mock import Mock, patch
from model_updated_interface2 import Model
import pickle
import os

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

def test_save_model(setup_model, tmpdir):
    """Test that a model can be saved correctly to a file."""
    # Setting up mock model data
    setup_model.model_formula = {"formula": "y = 3x1 + 5x2 + 2"}
    setup_model.model_metrics = {"mse": 0.03, "r2": 0.95}
    setup_model.columns_selected = ["x1", "x2"]
    setup_model.output_column = "y"
    setup_model.description_saved = {"description": "Test model description"}
    
    # Mock the save file dialog to return a temporary file path
    model_file = tmpdir.join("saved_model.pkl")
    with patch("tkinter.filedialog.asksaveasfilename", return_value=str(model_file)):
        # Mock messagebox to suppress UI interaction
        with patch("tkinter.messagebox.showinfo") as mock_showinfo:
            setup_model.save_model()

            # Ensure showinfo was called with the expected message
            mock_showinfo.assert_called_once_with("Model Saved", f"Model saved at {model_file}")

    # Verify that the file was created
    assert os.path.exists(model_file), "The model file was not created."

    # Load the saved model to verify its contents
    with open(model_file, "rb") as f:
        saved_data = pickle.load(f)
        assert saved_data["formula"] == setup_model.model_formula, "The saved formula does not match."
        assert saved_data["metrics"] == setup_model.model_metrics, "The saved metrics do not match."
        assert saved_data["input_columns"] == setup_model.columns_selected, "The saved input columns do not match."
        assert saved_data["output_column"] == setup_model.output_column, "The saved output column does not match."
        assert saved_data["description"] == setup_model.description_saved, "The saved description does not match."