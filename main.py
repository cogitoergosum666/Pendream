import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QSpinBox,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
import os
from PyQt5.QtCore import QCoreApplication
from interface import HandwritingInterface  # Ensure the main application is properly imported

# 设置 Qt 平台插件路径
plugin_path = os.path.join(os.path.dirname(sys.modules['PyQt5'].__file__), 'Qt5', 'plugins')
QCoreApplication.addLibraryPath(plugin_path)

class EducationAppMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Education App - Starting Menu")
        self.setGeometry(100, 100, 400, 400)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Title Graph (Decoration)
        self.graph_label = QLabel(self)
        self.graph_label.setPixmap(QPixmap("title.png"))  # Set your default image path here
        self.graph_label.setFixedHeight(150)
        self.graph_label.setStyleSheet("border: none;")
        self.main_layout.addWidget(self.graph_label)

        # Title
        self.title_label = QLabel("Select Your Preferences", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(self.title_label)

        # Word Type Selection
        self.word_type_label = QLabel("Select Word Type:")
        self.word_type_combo = QComboBox()
        self.word_type_combo.addItems(["Mix", "Nouns", "Verbs", "Adjectives/Adverbs"])

        word_type_layout = QHBoxLayout()
        word_type_layout.addWidget(self.word_type_label)
        word_type_layout.addWidget(self.word_type_combo)
        self.main_layout.addLayout(word_type_layout)

        # Difficulty Selection
        self.difficulty_label = QLabel("Select Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["1", "2", "3"])

        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(self.difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        self.main_layout.addLayout(difficulty_layout)

        # Question Amount Selection
        self.amount_label = QLabel("Enter Number of Questions (1-100):")
        self.amount_spinbox = QSpinBox()
        self.amount_spinbox.setRange(1, 100)

        amount_layout = QHBoxLayout()
        amount_layout.addWidget(self.amount_label)
        amount_layout.addWidget(self.amount_spinbox)
        self.main_layout.addLayout(amount_layout)

        # Start Button
        self.start_button = QPushButton("Start Test")
        self.start_button.clicked.connect(self.start_test)
        self.main_layout.addWidget(self.start_button)

    def start_test(self):
        word_type = self.word_type_combo.currentText()
        difficulty = self.difficulty_combo.currentText()
        question_amount = self.amount_spinbox.value()
        if not (1 <= question_amount <= 100):
            QMessageBox.warning(self, "Invalid Input", "Please enter a number of questions between 1 and 100.")
            return
        print(f"Starting test with: \nWord Type: {word_type}\nDifficulty: {difficulty}\nQuestion Amount: {question_amount}")

        # Pass parameters to the main application
        self.open_main_application(word_type, difficulty, question_amount)

    def open_main_application(self, word_type, difficulty, question_amount):
        # Placeholder for integrating with the main application
        # Replace this with the actual import and initialization of your main application

        self.main_app = HandwritingInterface(word_type, int(difficulty), int(question_amount))
        self.main_app.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EducationAppMenu()
    window.show()
    sys.exit(app.exec_())
