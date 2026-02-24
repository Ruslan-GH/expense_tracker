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
    target = session.get(Category, cat_id)
    if target:
        # Завдяки cascade="all, delete-orphan", витрати видаляться автоматично
        session.delete(target)
        session.commit()
        print(f"Категорія '{target.name}' та всі її витрати видалені.")
    else:
        print("Категорію не знайдено.")

# Для Витрат
def add_expense(session, title, amount, category_id, description=None, currency="UAH", expense_date=None):
    if not expense_date:
        expense_date = date.today()

    new_exp = Expense(
        title=title,
        amount=amount,
        date=expense_date,
        category_id=category_id,
        description=description,
        currency=currency
    )
    session.add(new_exp)
    session.commit()
    print(f"Витрата '{title}' на суму {amount} {currency} додана.")

def get_all_expenses(session):
    return session.query(Expense).join(Category).all()

def update_expense(session, exp_id, new_amount=None, new_description=None):
    target = session.get(Expense, exp_id)
    if target:
        if new_amount:
            target.amount = new_amount
        if new_description:
            target.description = new_description
        session.commit()
        print(f"Витрата №{exp_id} оновлена.")
    else:
        print("Витрату не знайдено.")

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