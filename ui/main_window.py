from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from ui.start_page import StartPage
from ui.exercise_page import ExercisePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Application")
        self.setGeometry(300, 300, 800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.start_page = StartPage(self)
        self.exercise_page = ExercisePage(self)

        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.exercise_page)

        self.show_start_page()

    def show_start_page(self):
        self.stack.setCurrentWidget(self.start_page)

    def show_exercise_page(self):
        self.stack.setCurrentWidget(self.exercise_page)
