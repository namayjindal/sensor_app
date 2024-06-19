from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCalendarWidget, QPushButton
from PyQt5.QtCore import QDate

class StartPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        self.school_name_label = QLabel("School Name:")
        self.school_name_input = QLineEdit()

        self.date_label = QLabel("Date:")
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.goto_exercise_page)

        layout.addWidget(self.school_name_label)
        layout.addWidget(self.school_name_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.calendar)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def goto_exercise_page(self):
        school_name = self.school_name_input.text()
        date = self.calendar.selectedDate().toString("dd/MM/yyyy")

        self.parent.exercise_page.set_initial_data(school_name, date)
        self.parent.show_exercise_page()
