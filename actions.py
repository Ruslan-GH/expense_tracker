from sqlalchemy.exc import SQLAlchemyError

from models import Category, Expense
from datetime import date

# Для Категорій
def add_category(session, name):
    existing = session.query(Category).filter(Category.name.ilike(name)).first()
    if existing:
        print(f"Категорія '{name}' вже існує.")
        return

    new_cat = Category(name=name)
    session.add(new_cat)
    session.commit()
    print(f"Категорія '{name}' додана.")

def get_all_categories(session):
    return session.query(Category).all()

def update_category_name(session, cat_id, new_name):
    target = session.get(Category, cat_id)
    if target:
        target.name = new_name
        session.commit()
        print(f"Категорію оновлено на '{new_name}'.")
    else:
        print("Категорію не знайдено.")

def delete_category(session, cat_id):
    try:
        category = session.get(Category, cat_id)
        if not category:
            print(f"Помилка: Категорію з ID {cat_id} не знайдено.")
            return

        expense_count = len(category.expenses)

        if expense_count > 0:
            print(f"Зверніть увагу, що в категорії '{category.name}' знайдено {expense_count} витрат.")
            confirm = input(f"Ви впевнені, що хочете видалити її разом з усіма витратами? (y/n): ")
            if confirm.lower() != 'y':
                print("Видалення скасовано.")
                return

        session.delete(category)
        session.commit()
        print(f"Категорію '{category.name}' та всі пов'язані витрати успішно видалено.")

    except Exception as e:
        session.rollback()
        print(f"Помилка при видаленні: {e}")

# Для Витрат
def add_expense(session, title, amount, category_id, description=None, currency="UAH", expense_date=None):
    if amount <= 0:
        print("Сума витрати повинна бути більшою за нуль!")
        return

    try:
        category = session.get(Category, category_id)
        if not category:
            print(f"Категорії з ID {category_id} не існує! Спочатку створіть категорію.")
            return

        new_expense = Expense(
            title=title,
            amount=amount,
            category_id=category_id,
            description=description
        )

        session.add(new_expense)
        session.commit()
        print(f"Витрату '{title}' на суму {amount} успішно додано до категорії '{category.name}'.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Критична помилка бази даних: {e}")
    except Exception as e:
        print(f"Сталася невідома помилка: {e}")

def get_all_expenses(session):
    return session.query(Expense).join(Category).all()


def update_expense(session, expense_id, title=None, amount=None, category_id=None,
                   expense_date=None, description=None, currency=None):
    try:
        expense = session.get(Expense, expense_id)
        if not expense:
            print(f"Витрату з ID {expense_id} не знайдено.")
            return

        # Використовуємо "is not None", щоб дозволити зміну на будь-яке валідне значення
        if title is not None:
            expense.title = title

        if amount is not None:
            if amount <= 0:
                print("Сума має бути більшою за 0.")
            else:
                expense.amount = amount

        if category_id is not None:
            # Перевіряємо чи існує нова категорія
            if session.get(Category, category_id):
                expense.category_id = category_id
            else:
                print(f"Категорії {category_id} не існує.")

        if expense_date is not None:
            expense.date = expense_date

        if description is not None:
            expense.description = description

        if currency is not None:
            expense.currency = currency.upper()

        session.commit()
        print(f"Витрату ID {expense_id} успішно оновлено.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Помилка БД при оновленні: {e}")

def delete_expense(session, exp_id):
    target = session.get(Expense, exp_id)
    if target:
        session.delete(target)
        session.commit()
        print(f"Витрата №{exp_id} видалена.")
    else:
        print("Витрату не знайдено.")


def display_expenses(expenses):
    if not expenses:
        print("\n--- Список витрат порожній ---")
        return

    print("\n" + "=" * 70)
    print(f"{'ID':<4} | {'Дата':<10} | {'Назва':<15} | {'Сума':<10} | {'Категорія'}")
    print("-" * 70)

    for exp in expenses:
        # Зверни увагу: exp.category.name працює завдяки relationship в моделях!
        print(f"{exp.id:<4} | {exp.date} | {exp.title:<15} | {exp.amount:<10.2f} | {exp.category.name}")
    print("=" * 70 + "\n")