import config

def save_report_to_file(data_text):

    try:
        with open(config.REPORT_FILE_PATH, mode="a", encoding=config.DEFAULT_ENCODING) as file:
            file.write("\n" + "="*30 + "\n")
            file.write(data_text)
            file.write("\n" + "="*30 + "\n")
        print(f"Звіт успішно збережено у файл: {config.REPORT_FILE_PATH}")
    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}")