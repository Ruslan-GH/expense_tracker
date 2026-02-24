from database import get_session, init_db
import reports, actions, exporter
from datetime import date

from data_example import seed_data

def main():
    init_db()

    seed_data()

    session = get_session()

    while True:
        print("=" * 30)
        print("Опції для роботи з категоріями")
        print("-" * 30)
        print("1. Додати категорію")
        print("2. Показати всі категорії")
        print("3. Оновити назву категорії")
        print("4. Видалити категорію")
        print("=" * 30)
        print("Опції для роботи з витратами")
        print("-" * 30)
        print("5. Додати витрати")
        print("6. Показати всі витрати")
        print("7. Оновити витрати")
        print("8. Видалити витрати")
        print("=" * 30)
        print("Опції формування звітів")
        print("-" * 30)
        print("9. Відфільтрувати витрати за датою / назвою / категорією")
        print("10. Отримати максимальну витрату по категорії")
        print("11. Отримати максимальну витрату по періоду")
        print("12. Отримати мінімальну витрату по категорії")
        print("13. Отримати мінімальну витрату по періоду")
        print("14. Отримати суму по кожній з категорій")
        print("15. Отримати топ категорію")
        print("16. Отримати середні витрати за період")

        choice = input("Оберіть пункт: ")

        # --- КАТЕГОРІЇ ---
        if choice == "1":
            name = input("Назва нової категорії: ")
            actions.add_category(session, name)

        elif choice == "2":
            categories = actions.get_all_categories(session)
            # for c in categories: print(f"ID: {c.id} | {c.name}")
            report_text = "СПИСОК КАТЕГОРІЙ:\n"
            report_text += "-" * 20 + "\n"

            for c in categories:
                line = f"ID: {c.id} | {c.name}"
                print(line)  # Виводимо в консоль
                report_text += line + "\n"  # Додаємо в текст звіту

            save_choice = input("\nЗберегти цей список у файл? (y/n): ")
            if save_choice.lower() == 'y':
                exporter.save_report_to_file(report_text)

        elif choice == "3":
            try:
                c_id = int(input("ID категорії для зміни: "))
                new_name = input("Нова назва: ")
                actions.update_category_name(session, c_id, new_name)
            except ValueError:
                print("Помилка: введіть числове ID")

        elif choice == "4":
            try:
                c_id = int(input("ID категорії для видалення: "))
                actions.delete_category(session, c_id)
            except ValueError:
                print("Помилка: введіть числове ID")

        # --- ВИТРАТИ ---
        elif choice == "5":
            try:
                cats = actions.get_all_categories(session)
                for c in cats: print(f"{c.id}: {c.name}")
                c_id = int(input("Оберіть ID категорії: "))
                title = input("Назва витрати: ")
                amount = float(input("Сума: "))
                desc = input("Опис (опційно): ")
                actions.add_expense(session, title, amount, c_id, description=desc)
            except ValueError:
                print("Помилка у форматі даних.")

        elif choice == "6":
            expenses = actions.get_all_expenses(session)
            actions.display_expenses(expenses)

            save_choice = input("\nЗберегти цей список у файл? (y/n): ")
            if save_choice.lower() == 'y':
                header = f"{'ID':<4} | {'Дата':<10} | {'Назва':<15} | {'Сума':<10} | {'Категорія'}\n"
                separator = "-" * 70 + "\n"

                report_text = "ЗВІТ ПО ВСІХ ВИТРАТАХ\n" + separator + header + separator

                for exp in expenses:
                    line = f"{exp.id:<4} | {exp.date} | {exp.title:<15} | {exp.amount:<10.2f} | {exp.category.name}\n"
                    report_text += line

                report_text += separator

                exporter.save_report_to_file(report_text)

        elif choice == "7":
            try:
                e_id = int(input("ID витрати для оновлення: "))
                new_sum = input("Нова сума (Enter щоб пропустити): ")
                new_sum = float(new_sum) if new_sum else None
                new_desc = input("Новий опис: ")
                actions.update_expense(session, e_id, new_sum, new_desc)
            except ValueError:
                print("Помилка оновлення.")

        elif choice == "8":
            try:
                e_id = int(input("ID витрати для видалення: "))
                actions.delete_expense(session, e_id)
            except ValueError:
                print("Помилка ID.")

        # --- ЗВІТИ ---
        elif choice == "9":
            s_date = input("З якої дати (РРРР-ММ-ДД) або Enter: ")
            e_date = input("По яку дату (РРРР-ММ-ДД) або Enter: ")
            title = input("Назва або Enter: ")
            cat = input("Категорія або Enter: ")

            start = date.fromisoformat(s_date) if s_date else None
            end = date.fromisoformat(e_date) if e_date else None

            res = reports.filter_expenses(session, start, end, title, cat)
            actions.display_expenses(res)

        elif choice == "10":
            for name, val in reports.get_max_expense_per_category(session):
                print(f"{name}: {val:.2f}")

        elif choice == "11":
            try:
                sd = date.fromisoformat(input("З якої дати (РРРР-ММ-ДД): "))
                ed = date.fromisoformat(input("По яку дату (РРРР-ММ-ДД): "))
                res = reports.get_max_expense_in_period(session, sd, ed)
                print(f"Максимальна витрата: {res if res else 0:.2f}")
            except ValueError:
                print("Невірний формат дати.")

        elif choice == "12":
            for name, val in reports.get_min_expense_per_category(session):
                print(f"{name}: {val:.2f}")

        elif choice == "13":
            try:
                sd = date.fromisoformat(input("З якої дати (РРРР-ММ-ДД): "))
                ed = date.fromisoformat(input("По яку дату (РРРР-ММ-ДД): "))
                res = reports.get_min_expense_in_period(session, sd, ed)
                print(f"Мінімальна витрата: {res if res else 0:.2f}")
            except ValueError:
                print("Невірний формат дати.")

        elif choice == "14":
            for name, total in reports.get_totals_by_category(session):
                print(f"{name}: {total:.2f}")

        elif choice == "15":
            res = reports.get_top_category(session)
            if res: print(f"ТОП Категорія: {res[0]} (Сума: {res[1]:.2f})")

        elif choice == "16":
            try:
                sd = date.fromisoformat(input("З якої дати (РРРР-ММ-ДД): "))
                ed = date.fromisoformat(input("По яку дату (РРРР-ММ-ДД): "))
                avg = reports.get_daily_average_in_period(session, sd, ed)
                print(f"Середні витрати на день: {avg:.2f}")
            except ValueError:
                print("Помилка дати.")

        elif choice == "0":
            print("Вихід...")
            break
        else:
            print("Невірний пункт.")

    session.close()


if __name__ == "__main__":
    main()