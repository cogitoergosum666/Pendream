import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PIL import Image

import os
from PyQt5.QtCore import QCoreApplication

# set dir when qt not work
plugin_path = os.path.join(os.path.dirname(sys.modules['PyQt5'].__file__), 'Qt5', 'plugins')
QCoreApplication.addLibraryPath(plugin_path)

# Import your classes
from Question_set import Question_set
from writing import HandwritingApp
from OCR_model import OCR_model

class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.questions_list = []
        self.final_score = 0
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Final Report")
        layout = QVBoxLayout()

        # show label
        self.score_label = QLabel("Final Score: 0")
        layout.addWidget(self.score_label)
        
        # show question
        self.questions_display = QTextEdit()
        self.questions_display.setReadOnly(True)
        layout.addWidget(self.questions_display)

        # back to main page
        self.return_button = QPushButton("Return to Main Window")
        self.return_button.clicked.connect(self.close)
        layout.addWidget(self.return_button)


        self.setLayout(layout)

    def display_report(self):
        """显示问题列表"""
        # renew the score board
        self.score_label.setText(f"Final Score: {self.final_score}")

        if self.questions_list:
            questions_text = "\n".join(
                [f"Q{i+1}: {q['question']} Answer{i+1}: {q['answer']} \n(Hint: {q['hint']}, Difficulty: {q['difficulty']})"
                 for i, q in enumerate(self.questions_list)]
            )
            if self.final_score/(len(self.questions_list)) == 1:
                questions_text += "\nPerfect! You've done a great job!"
                print("Perfect! You've done a great job!")
            elif self.final_score/(len(self.questions_list)) >= 0.6 and self.final_score/(len(self.questions_list)) <= 0.99:
                questions_text += "\nGood job! Keep practicing!"
                print("Good job! Keep practicing!")
            elif self.final_score/(len(self.questions_list)) >= 0.3 and self.final_score/(len(self.questions_list)) <= 0.59:
                questions_text += "\nTry harder! You can do it better!"
                print("Try harder! You can do it better!")
            else:
                questions_text += "\nPractice more! You can make it!"
                print("Practice more! You can make it!")
            self.questions_display.setText(questions_text)
            
        else:
            self.questions_display.setText("No questions available.")

class HandwritingInterface(QWidget):
    def __init__(self, word_type = 'mix', diff = 1, question_len = 10):
        super().__init__()
        self.question_set = Question_set(word_type, question_len, diff)
        self.handwriting_app = HandwritingApp()
        self.questions_list = []
        self.ocr_model = OCR_model()
        self.score = 0
        self.init_ui()
        self.current_question_index = 0
        self.load_next_question()

    def load_next_question(self):
        """Load the next question from the question set"""
        questions = list(self.question_set.questions.items())
        if self.current_question_index < len(questions):
            self.current_question = questions[self.current_question_index]

            question, hint, diff_level = self.current_question[0][0], self.current_question[0][1], self.current_question[0][2]
            answer = self.current_question[1]
            self.question_label.setText(f"Question: {question}")
            self.hint_label.setText(f"Hint: {hint}")
            self.level_label.setText(f"Difficulty Level: {diff_level}")

            self.questions_list.append({
                "question": question,
                "hint": hint,
                "difficulty": diff_level,
                "answer": answer
            })

            self.current_question_index += 1
        else:
            self.question_label.setText("No more questions available.")
            self.hint_label.setText("")
            self.level_label.setText("")

    def init_ui(self):
        self.setWindowTitle("Handwriting Answer App")

        layout = QVBoxLayout()

        # Question Display
        self.question_label = QLabel("Question:")
        layout.addWidget(self.question_label)

        # Hint Display
        self.hint_label = QLabel("Hint:")
        layout.addWidget(self.hint_label)

        # Difficulty Level Display
        self.level_label = QLabel("Difficulty Level:")
        layout.addWidget(self.level_label)

        # Score Display
        self.score_label = QLabel("Score: 0")
        layout.addWidget(self.score_label)

        # Start Handwriting Button
        self.start_handwriting_btn = QPushButton("Start Handwriting")
        self.start_handwriting_btn.clicked.connect(self.open_handwriting_board)
        layout.addWidget(self.start_handwriting_btn)

        # Evaluate Button
        self.evaluate_btn = QPushButton("Evaluate Answer")
        self.evaluate_btn.clicked.connect(self.evaluate_answer)
        layout.addWidget(self.evaluate_btn)

        # Result Display
        self.result_label = QLabel("Result: ")
        layout.addWidget(self.result_label)

        # Handwriting Answer Display
        self.handwriting_answer_label = QLabel("Your Answer: ")
        layout.addWidget(self.handwriting_answer_label)

        # Correct Answer Display
        self.correct_answer_label = QLabel("Correct Answer: ")
        layout.addWidget(self.correct_answer_label)

        # Next question Button
        self.nextquestion_btn = QPushButton("Next Question")
        self.nextquestion_btn.clicked.connect(self.load_next_question)
        layout.addWidget(self.nextquestion_btn)

        # Final report Button
        self.finalreport_btn = QPushButton("Final Report")
        self.finalreport_window = ReportWindow()
        self.finalreport_btn.clicked.connect(self.open_report_window)
        layout.addWidget(self.finalreport_btn)

        # Exit Button
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close_application)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

    def open_report_window(self):
        """Open the second window and pass the question list"""
        self.finalreport_window.questions_list = self.questions_list  # pass question list
        self.finalreport_window.final_score = self.score  # pass score
        self.finalreport_window.display_report()  # renew screen
        self.finalreport_window.show()

    def open_handwriting_board(self):
        """Open the handwriting board"""
        self.handwriting_app.writing_board()

    def evaluate_answer(self):
        """Evaluate the answer using the OCR model"""
        ocr_result = self.ocr_model.start_OCR()
        ocr_result = ocr_result.replace(" ", "") 
        print(ocr_result)
        
        if self.current_question:
            correct_answer = self.current_question[1]
            self.handwriting_answer_label.setText(f"Your Answer: {ocr_result}")
            if ocr_result.strip() == correct_answer.strip():
                self.result_label.setText("Result: True")
                self.score += 1
                self.score_label.setText(f"Score: {self.score}")
            else:
                self.result_label.setText("Result: False")
            
            self.correct_answer_label.setText(f"Correct Answer: {correct_answer}")
        else:
            self.result_label.setText("Result: No question loaded.")
            self.correct_answer_label.setText("Correct Answer: N/A")
            
    def close_application(self):
        """Close the application"""
        QApplication.quit()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = HandwritingInterface()
#     main_window.show()
#     sys.exit(app.exec_())
