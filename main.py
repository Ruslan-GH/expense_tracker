from database import get_session, init_db
import reports, actions, exporter

from data_example import seed_data
from models import Expense
from utils import get_positive_decimal
from datetime import datetime, date


def main():
    init_db()

    seed_data()

    session = get_session()

    while True:
        print("   ГОЛОВНЕ МЕНЮ")
        print("═" * 30)
        print("1. Опції для роботи з категоріями")
        print("2. Опції для роботи з витратами")
        print("3. Опції формування звітів")
        print("0. Вихід з програми")
        print("═" * 30)

        choice = input("Оберіть пункт: ")

        if choice == "1":
            menu_categories(session)
        elif choice == "2":
            menu_expenses(session)
        elif choice == "3":
            menu_reports(session)
        elif choice == "0":
            print("Завершення роботи.")
            break
        else:
            print("Невірний вибір!")

    session.close()

def menu_categories(session):
    while True:
        print()
        print("Опції для роботи з категоріями")
        print("-" * 30)
        print("1. Додати категорію")
        print("2. Показати всі категорії")
        print("3. Оновити назву категорії")
        print("4. Видалити категорію")
        print("0. Назад")
        print("=" * 30)

        choice = input("\nОберіть дію: ")
        # --- КАТЕГОРІЇ ---
        if choice == "1":
            name = input("Назва нової категорії: ")
            actions.add_category(session, name)

        elif choice == "2":
            categories = actions.get_all_categories(session)

            print("\n" + "─" * 20)
            print("СПИСОК КАТЕГОРІЙ:")
            print("─" * 20)
            for c in categories:
                print(f"ID: {c.id:<3} | Назва: {c.name}")
            print("─" * 20)

            save_choice = input("\nДля експорту списку оберіть введіть формат - csv, або json. Для відмови введіть  - no: ").lower().strip()

            if save_choice == "csv":
                headers = ["ID", "Назва"]
                # Формуємо список списків для CSV
                data_rows = [[c.id, c.name] for c in categories]
                exporter.save_to_csv("all_categories", data_rows, headers)

            elif save_choice == "json":
                # Формуємо список словників для JSON
                data_dicts = [{"id": c.id, "name": c.name} for c in categories]
                exporter.save_to_json("all_categories", data_dicts)

            else:
                print("Експорт скасовано.")

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

        elif choice == "0":
            break

def menu_expenses(session):
    while True:
        print()
        print("Опції для роботи з витратами")
        print("-" * 30)
        print("1. Додати витрати")
        print("2. Показати всі витрати")
        print("3. Оновити витрати")
        print("4. Видалити витрати")
        print("0. Назад")
        print("=" * 30)

        choice = input("\nОберіть дію: ")
        # --- ВИТРАТИ ---
        if choice == "1":
            try:
                cats = actions.get_all_categories(session)
                for c in cats:
                    print(f"{c.id}: {c.name}")

                c_id = int(input("Оберіть ID категорії: "))
                title = input("Назва витрати: ")

                amount = get_positive_decimal(input("Сума: "))

                desc = input("Опис (опційно): ")
                actions.add_expense(session, title, amount, c_id, description=desc, expense_date = date.today())
            except ValueError:
                print("Помилка у форматі даних.")

        elif choice == "2":
            expenses = actions.get_all_expenses(session)
            actions.display_expenses(expenses)

            save_choice = input("\nДля експорту списку оберіть введіть формат - csv, або json. Для відмови введіть  - no: ").lower().strip()

            if save_choice == "csv":
                headers = ["ID", "Дата", "Назва", "Сума", "Категорія"]
                data_rows = [[e.id, str(e.date), e.title, e.amount, e.category.name] for e in expenses]
                exporter.save_to_csv("all_expenses", data_rows, headers)
            elif save_choice == "json":
                data_dicts = [{
                    "id": e.id,
                    "date": str(e.date),
                    "title": e.title,
                    "amount": e.amount,
                    "category": e.category.name
                } for e in expenses]
                exporter.save_to_json("all_expenses_dump", data_dicts)
            else:
                print("Експорт скасовано.")

        elif choice == "3":
            try:
                e_id_input = input("Введіть ID витрати для редагування (або 0 для скасування): ")
                if e_id_input == "0": continue

                e_id = int(e_id_input)
                exp = session.get(Expense, e_id)

                if not exp:
                    print(f"Витрату з ID {e_id} не знайдено.")
                    continue

                print(f"\nРедагування витрати #{e_id} (Enter — залишити без змін)")

                # Назва
                new_title = input(f"Нова назва [{exp.title}]: ") or None

                # Сума
                new_amount_raw = input(f"Нова сума [{exp.amount}]: ")
                new_amount = None
                if new_amount_raw:
                    new_amount = float(new_amount_raw)
                    if new_amount <= 0:
                        print("Сума повинна бути > 0.")
                        new_amount = None

                # Категорія
                new_cat_raw = input(f"Новий ID категорії [{exp.category_id}]: ")
                new_cat = int(new_cat_raw) if new_cat_raw else None

                # Дата (з окремою обробкою помилки формату)
                new_date = None
                new_date_raw = input(f"Нова дата (РРРР-ММ-ДД) [{exp.date}]: ")
                if new_date_raw:
                    try:
                        new_date = date.fromisoformat(new_date_raw)
                    except ValueError:
                        print("Невірний формат дати. Використано стару дату.")

                # Опис та Валюта
                new_desc = input(f"Новий опис [{exp.description or 'немає'}]: ") or None
                new_curr = input(f"Нова валюта [{exp.currency}]: ") or None

                # Виклик оновлення
                actions.update_expense(
                    session, e_id,
                    title=new_title,
                    amount=new_amount,
                    category_id=new_cat,
                    expense_date=new_date,
                    description=new_desc,
                    currency=new_curr
                )
            except ValueError:
                print("Помилка оновлення.")

        elif choice == "4":
            try:
                e_id = int(input("ID витрати для видалення: "))
                actions.delete_expense(session, e_id)
            except ValueError:
                print("Помилка ID.")
        elif choice == "0":
            break

def menu_reports(session):
    while True:
        print()
        print("Опції формування звітів")
        print("-" * 30)
        print("1. Відфільтрувати витрати за датою / назвою / категорією")
        print("2. Отримати максимальну витрату по категорії")
        print("3. Отримати максимальну витрату по періоду")
        print("4. Отримати мінімальну витрату по категорії")
        print("5. Отримати мінімальну витрату по періоду")
        print("6. Отримати суму по кожній з категорій")
        print("7. Отримати топ категорію")
        print("8. Отримати середні витрати за період")
        print("0. Назад")

        choice = input("\nОберіть звіт: ")
        # --- ЗВІТИ ---
        if choice == "1":
            s_date = input("З якої дати (РРРР-ММ-ДД) або Enter: ")
            e_date = input("По яку дату (РРРР-ММ-ДД) або Enter: ")
            title = input("Назва витрати: ")

            print("\nДоступні категорії для пошуку:")
            cats = actions.get_all_categories(session)
            if cats:
                print(", ".join([c.name for c in cats]))
            else:
                print("Список категорій порожній.")


            cat = input("Категорія або Enter: ").strip()

            start = date.fromisoformat(s_date) if s_date else None
            end = date.fromisoformat(e_date) if e_date else None

            res = reports.filter_expenses(session, start, end, title, cat)
            actions.display_expenses(res)

        elif choice == "2":
            for name, val in reports.get_max_expense_per_category(session):
                print(f"{name}: {val:.2f}")

        elif choice == "3":
            try:
                sd = date.fromisoformat(input("З якої дати (РРРР-ММ-ДД): "))
                ed = date.fromisoformat(input("По яку дату (РРРР-ММ-ДД): "))
                res = reports.get_max_expense_in_period(session, sd, ed)
                print(f"Максимальна витрата: {res if res else 0:.2f}")
            except ValueError:
                print("Невірний формат дати.")

        elif choice == "4":
            for name, val in reports.get_min_expense_per_category(session):
                print(f"{name}: {val:.2f}")

        elif choice == "5":
            try:
                sd = date.fromisoformat(input("З якої дати (РРРР-ММ-ДД): "))
                ed = date.fromisoformat(input("По яку дату (РРРР-ММ-ДД): "))
                res = reports.get_min_expense_in_period(session, sd, ed)
                print(f"Мінімальна витрата: {res if res else 0:.2f}")
            except ValueError:
                print("Невірний формат дати.")

        elif choice == "6":
            for name, total in reports.get_totals_by_category(session):
                print(f"{name}: {total:.2f}")

        elif choice == "7":
            res = reports.get_top_category(session)
            if res: print(f"ТОП Категорія: {res[0]} (Сума: {res[1]:.2f})")

        elif choice == "8":
            try:
                sd = date.fromisoformat(input("З якої дати (РРРР-ММ-ДД): "))
                ed = date.fromisoformat(input("По яку дату (РРРР-ММ-ДД): "))
                avg = reports.get_daily_average_in_period(session, sd, ed)
                print(f"Середні витрати на день: {avg:.2f}")
            except ValueError:
                print("Помилка дати.")

        elif choice == "0":
            break
        else:
            print("Невірний пункт.")

if __name__ == "__main__":
    main()