import json
import os

class DataManager:
    def __init__(self):
        self.data_file = "./sensor_data/data.json"
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def save_data(self, school_name, date, grade, exercise, label, csv_filename):
        data = {
            "school_name": school_name,
            "date": date,
            "grade": grade,
            "exercise": exercise,
            "label": label,
            "csv_filename": csv_filename
        }

        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        existing_data.append(data)

        with open(self.data_file, 'w') as file:
            json.dump(existing_data, file, indent=4)

    def discard_data(self, csv_filename):
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
