from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from sensor.sensor_manager import SensorManager
from utils.data_manager import DataManager
import asyncio
from utils.constants import TARGET_SENSOR_NAMES, UART_RX_CHAR_UUID_1, UART_RX_CHAR_UUID_2, UART_RX_CHAR_UUID_3, UART_RX_CHAR_UUID_4

class ExercisePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.sensor_manager = SensorManager()
        self.data_manager = DataManager()

        layout = QVBoxLayout()

        self.grade_label = QLabel("Grade:")
        self.grade_input = QLineEdit()

        self.exercise_label = QLabel("Exercise:")
        self.exercise_dropdown = QComboBox()
        self.exercise_dropdown.addItems([
            "Exercise 1", "Exercise 2", "Exercise 3", "Exercise 4", "Exercise 5",
            "Exercise 6", "Exercise 7", "Exercise 8", "Exercise 9", "Exercise 10",
            "Exercise 11", "Exercise 12", "Exercise 13", "Exercise 14", "Exercise 15",
            "Exercise 16", "Exercise 17", "Exercise 18", "Exercise 19"
        ])

        self.connect_button = QPushButton("Connect to Sensors")
        self.connect_button.clicked.connect(self.connect_sensors)

        self.start_button = QPushButton("Start Exercise")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_exercise)

        self.stop_button = QPushButton("Stop Exercise")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_exercise)

        layout.addWidget(self.grade_label)
        layout.addWidget(self.grade_input)
        layout.addWidget(self.exercise_label)
        layout.addWidget(self.exercise_dropdown)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def set_initial_data(self, school_name, date):
        self.school_name = school_name
        self.date = date

    async def connect_sensors(self):
        await self.sensor_manager.scan_devices()
        self.sensor_manager.filter_devices(TARGET_SENSOR_NAMES)

        tasks = []
        for device in self.sensor_manager.devices:
            if device.name == "Sense Right Hand":
                tasks.append(self.sensor_manager.connect_to_sensor(device, 1, UART_RX_CHAR_UUID_1))
            elif device.name == "Sense Left Hand":
                tasks.append(self.sensor_manager.connect_to_sensor(device, 2, UART_RX_CHAR_UUID_2))
            elif device.name == "Sense Right Leg":
                tasks.append(self.sensor_manager.connect_to_sensor(device, 3, UART_RX_CHAR_UUID_3))
            elif device.name == "Sense Left Leg":
                tasks.append(self.sensor_manager.connect_to_sensor(device, 4, UART_RX_CHAR_UUID_4))

        await asyncio.gather(*tasks)

         #asyncio.run(asyncio.gather(*tasks))

        self.start_button.setEnabled(True)

    def start_exercise(self):
        grade = self.grade_input.text()
        exercise = self.exercise_dropdown.currentText()

        asyncio.run(self.sensor_manager.start_tracking(exercise, grade))

        self.stop_button.setEnabled(True)

    def stop_exercise(self):
        self.stop_button.setEnabled(False)
        label, ok = QInputDialog.getItem(self, "Label Data", "Select Label:", ["Good", "Idle", "Bad"], 0, False)
        if ok:
            asyncio.run(self.sensor_manager.stop_tracking(label))
            self.data_manager.save_data(self.school_name, self.date, self.grade_input.text(), self.exercise_dropdown.currentText(), label, self.sensor_manager.csv_filename)
            QMessageBox.information(self, "Success", "Data saved successfully!")
        else:
            self.sensor_manager.discard_data()
            QMessageBox.information(self, "Data Discarded", "The exercise data has been discarded.")

        self.parent.show_start_page()
