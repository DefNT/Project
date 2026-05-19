import csv
import os

class FileHandler:
    @staticmethod
    def read_csv(filepath):
        if not os.path.isfile(filepath): return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def write_csv(filepath, data, fieldnames):
        if not data: return
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)