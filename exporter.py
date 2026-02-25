import csv
import json
import os
import config

def save_to_csv(filename, data, headers):
    file_path = os.path.join(config.EXPORT_DIR, f"{filename}.csv")
    try:
        with open(file_path, mode="w", newline="", encoding=config.DEFAULT_ENCODING) as f:
            writer = csv.writer(f, delimiter=';') # Крапка з комою краща для Excel
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Звіт збережено: {file_path}")
    except Exception as e:
        print(f"Помилка CSV експорту: {e}")

def save_to_json(filename, data):
    file_path = os.path.join(config.EXPORT_DIR, f"{filename}.json")
    try:
        with open(file_path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Звіт збережено: {file_path}")
    except Exception as e:
        print(f"Помилка JSON експорту: {e}")