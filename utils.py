def get_positive_decimal(prompt):
    while True:
        try:
            user_input = input(prompt).replace(',', '.')
            val = float(user_input)

            if val <= 0:
                print("Сума повинна бути більшою за нуль.")
                continue

            return val

        except ValueError:
            print("Невірний формат суми. Введіть число, наприклад 42.42")