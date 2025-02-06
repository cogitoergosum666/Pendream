import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from main import EducationAppMenu
from unittest.mock import patch
import sys

@pytest.fixture
def app():
    return QApplication(sys.argv)

@pytest.fixture
def main_window(app):
    window = EducationAppMenu()
    return window

def test_initial_ui_state(main_window):
    """Test the initial state of the UI components."""
    assert main_window.word_type_combo.currentText() == "Mix"
    assert main_window.difficulty_combo.currentText() == "1"
    assert main_window.amount_spinbox.value() == 1

def test_word_type_selection(main_window):
    """Test selecting a word type from the combo box."""
    main_window.word_type_combo.setCurrentIndex(1)  # Select "Nouns"
    assert main_window.word_type_combo.currentText() == "Nouns"

def test_difficulty_selection(main_window):
    """Test selecting a difficulty level from the combo box."""
    main_window.difficulty_combo.setCurrentIndex(2)  # Select "3"
    assert main_window.difficulty_combo.currentText() == "3"

def test_question_amount_input(main_window):
    """Test setting the number of questions in the spinbox."""
    main_window.amount_spinbox.setValue(50)
    assert main_window.amount_spinbox.value() == 50

# def test_start_button_with_valid_input(main_window, qtbot):
#     """Test clicking the start button with valid inputs."""
#     main_window.word_type_combo.setCurrentIndex(0)  # Mix
#     main_window.difficulty_combo.setCurrentIndex(1)  # 2
#     main_window.amount_spinbox.setValue(10)

#     with patch("main.EducationAppMenu.open_main_application") as mock_open_app:
#         qtbot.mouseClick(main_window.start_button, Qt.LeftButton)
#         mock_open_app.assert_called_once_with("Mix", "2", 10)

# def test_start_button_with_invalid_input(main_window, qtbot):
#     """Test clicking the start button with invalid inputs."""
#     main_window.amount_spinbox.setValue(101)  # Invalid value

#     # with patch("PyQt5.QtWidgets.QMessageBox.warning") as mock_warning:
#     #     qtbot.mouseClick(main_window.start_button, Qt.LeftButton)
#     #     mock_warning.assert_called_once_with(
#     #         main_window, "Invalid Input", "Please enter a number of questions between 1 and 100."
#     #     )

def test_open_main_application(main_window):
    """Test the open_main_application method."""
    with patch("main.HandwritingInterface") as mock_interface:
        main_window.open_main_application("Mix", "1", 10)
        mock_interface.assert_called_once_with("Mix", 1, 10)
        mock_interface().show.assert_called_once()
