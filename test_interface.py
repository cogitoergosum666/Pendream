from interface import HandwritingInterface, ReportWindow
import pytest
import sys
import os
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
from unittest.mock import MagicMock

# set dir when qt not work
plugin_path = os.path.join(os.path.dirname(sys.modules['PyQt5'].__file__), 'Qt5', 'plugins')
QCoreApplication.addLibraryPath(plugin_path)

app = QApplication(sys.argv)  # 初始化 QApplication

def test_init():
    """initialize"""
    print("Initializing ReportWindow...")
    window = ReportWindow()
    assert window.width() == 800
    assert window.height() == 600
    assert window.score_label.text() == "Final Score: 0"
    assert window.questions_display.toPlainText() == ""
    assert window.return_button.text() == "Return to Main Window"

def test_display_report_no_questions():
    """no question"""
    window = ReportWindow()
    window.display_report()
    assert window.score_label.text() == "Final Score: 0"
    assert window.questions_display.toPlainText() == "No questions available."

def test_display_report_with_questions():
    """with questions"""
    window = ReportWindow()
    window.questions_list = [
        {"question": 'p__te_n', "hint": 'a model considered worthy of imitation', "difficulty": 2, "answer": 'atr'},
        {"question": 'p__d_ction', "hint": 'the act or process of producing something', "difficulty": 2, "answer": 'rou'}
    ]
    window.final_score = 2  # 2 correct answers
    window.display_report()
    questions_text = window.questions_display.toPlainText()
    assert "Q1: p__te_n" in questions_text
    assert "Answer1: atr" in questions_text
    assert "Q2: p__d_ction" in questions_text
    assert "Answer2: rou" in questions_text

def test_perfect_feedback():
    """Perfect"""
    window = ReportWindow()
    window.questions_list = [
        {"question": 'p__te_n', "hint": 'a model considered worthy of imitation', "difficulty": 2, "answer": 'atr'}
    ]
    window.final_score = 1  # 1 correct answer
    window.display_report()
    questions_text = window.questions_display.toPlainText()
    assert "Perfect! You've done a great job!" in questions_text

def test_good_feedback():
    """Good"""
    window = ReportWindow()
    window.questions_list = [
        {"question": 'p__te_n', "hint": 'a model considered worthy of imitation', "difficulty": 2, "answer": 'atr'},
        {"question": 'p__d_ction', "hint": 'the act or process of producing something', "difficulty": 2, "answer": 'rou'},
        {"question": 'p__d_ction', "hint": 'the act or process of producing something', "difficulty": 2, "answer": 'rou'}
    ]
    window.final_score = 2  # 2 correct answer out of 3
    window.display_report()
    questions_text = window.questions_display.toPlainText()
    assert "Good job! Keep practicing!" in questions_text

def test_poor_feedback():
    """Try harder"""
    window = ReportWindow()
    # 添加问题
    window.questions_list = [
        {"question": 'p__te_n', "hint": 'a model considered worthy of imitation', "difficulty": 2, "answer": 'atr'},
        {"question": 'p__d_ction', "hint": 'the act or process of producing something', "difficulty": 2, "answer": 'rou'}
    ]
    window.final_score = 1  # 1 correct answers out of 2
    window.display_report()
    questions_text = window.questions_display.toPlainText()
    assert "Try harder! You can do it better!" in questions_text

def test_bad_feedback():
    """Practice more"""
    window = ReportWindow()
    # 添加问题
    window.questions_list = [
        {"question": 'p__te_n', "hint": 'a model considered worthy of imitation', "difficulty": 2, "answer": 'atr'},
        {"question": 'p__d_ction', "hint": 'the act or process of producing something', "difficulty": 2, "answer": 'rou'}
    ]
    window.final_score = 0  # 0 correct answers
    window.display_report()
    questions_text = window.questions_display.toPlainText()
    assert "Practice more! You can make it!" in questions_text

# def test_init_ui():
#     app = QApplication(sys.argv)
#     interface1 =  HandwritingInterface()
#     # Verify the window title
#     assert interface1.windowTitle() == "Handwriting Answer App"

#     # Check that all labels are properly initialized
#     #assert interface1.question_label.text() == "Question:"
#     assert "Question:" in interface1.question_label.text()
#     assert "Hint:" in interface1.hint_label.text()
#     assert "Difficulty Level:" in interface1.level_label.text()
#     assert "Score: 0" in interface1.score_label.text()
#     assert "Result: " in interface1.result_label.text()
#     assert "Your Answer: " in interface1.handwriting_answer_label.text()
#     assert "Correct Answer: " in interface1.correct_answer_label.text()

#test_init_ui()
# def test_load_next_question():
#     interface1 =  HandwritingInterface()
#     # Mock question_set
#     interface1.question_set.questions = {
#         ("Q1", "Hint1", 1): "Answer1",
#         ("Q2", "Hint2", 2): "Answer2"
#     }
#     interface1.load_next_question()

#     # Verify that the first question is loaded
#     assert interface1.question_label.text() == "Question: Q1"
#     assert interface1.hint_label.text() == "Hint: Hint1"
#     assert interface1.level_label.text() == "Difficulty Level: 1"
#     assert interface1.current_question_index == 1

#     # Load next question
#     interface1.load_next_question()
#     assert interface1.question_label.text() == "Question: Q2"
#     assert interface1.hint_label.text() == "Hint: Hint2"
#     assert interface1.level_label.text() == "Difficulty Level: 2"
#     assert interface1.current_question_index == 2

#     # No more questions
#     interface1.load_next_question()
#     assert interface1.question_label.text() == "No more questions available."
#     assert interface1.hint_label.text() == ""
#     assert interface1.level_label.text() == ""
# test_load_next_question()
def test_evaluate_answer_correct():
    interface1 =  HandwritingInterface()
    # Mock OCR and question
    interface1.ocr_model.start_OCR = MagicMock(return_value="Answer1")
    interface1.current_question = (("Q1", "Hint1", 1), "Answer1")

    interface1.evaluate_answer()

    # Verify correct evaluation
    assert interface1.result_label.text() == "Result: True"
    assert interface1.score == 1
    assert interface1.score_label.text() == "Score: 1"

def test_evaluate_answer_incorrect():
    interface1 =  HandwritingInterface()
    # Mock OCR and question
    interface1.ocr_model.start_OCR = MagicMock(return_value="WrongAnswer")
    interface1.current_question = (("Q1", "Hint1", 1), "Answer1")

    interface1.evaluate_answer()

    # Verify incorrect evaluation
    assert interface1.result_label.text() == "Result: False"
    assert interface1.score == 0
    assert interface1.correct_answer_label.text() == "Correct Answer: Answer1"

def test_open_handwriting_board():
    interface1 =  HandwritingInterface()
    # Mock handwriting_app
    interface1.handwriting_app.writing_board = MagicMock()

    interface1.open_handwriting_board()

    # Verify that the handwriting board is opened
    interface1.handwriting_app.writing_board.assert_called_once()

def test_open_report_window():
    interface1 =  HandwritingInterface()
    # Mock finalreport_window
    interface1.finalreport_window.display_report = MagicMock()
    interface1.finalreport_window.show = MagicMock()

    interface1.questions_list = ["Q1", "Q2"]
    interface1.score = 2
    interface1.open_report_window()

    # Verify the report window setup and display
    assert interface1.finalreport_window.questions_list == ["Q1", "Q2"]
    assert interface1.finalreport_window.final_score == 2
    interface1.finalreport_window.display_report.assert_called_once()
    interface1.finalreport_window.show.assert_called_once()

def test_close_application():
    interface1 =  HandwritingInterface()
    # Mock QApplication.quit
    QApplication.quit = MagicMock()

    interface1.close_application()

    # Verify that the application quits
    QApplication.quit.assert_called_once()
