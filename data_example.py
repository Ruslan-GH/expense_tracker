from models import Category, Expense
from database import get_session
from datetime import date, timedelta

def seed_data():
    session = get_session()

    # Перевірка, щоб не дублювати дані при кожному запуску
    if session.query(Category).count() > 0:
        session.close()
        return

    # Створюємо категорії
    categories = [
        Category(name="Продукти"),
        Category(name="Транспорт"),
        Category(name="Розваги"),
        Category(name="Здоров'я"),
        Category(name="Комуналка")
    ]
    session.add_all(categories)
    session.commit()

    # 2. Створюємо список витрат (Назва, Сума, Індекс категорії, Зміщення дати в днях)
    today = date.today()
    expenses_data = [
        ("Сільпо", 850.50, 0, 0),         # Сьогодні
        ("АТБ", 420.00, 0, -1),          # Вчора
        ("Бензин WOG", 1500.00, 1, -2),
        ("Кінотеатр", 350.00, 2, -3),
        ("Аптека", 120.00, 3, -4),
        ("Метро", 30.00, 1, 0),
        ("Вечеря в кафе", 600.00, 2, -1),
        ("Оренда квартири", 12000.00, 4, -15),
        ("Інтернет", 300.00, 4, -5),
        ("Яблука", 45.00, 0, -2),
        ("Таксі Bolt", 180.00, 1, -1),
        ("Вітаміни", 450.00, 3, -6),
        ("Концерт", 1200.00, 2, -10),
        ("Спортзал", 800.00, 2, -8),
        ("Заміна масла", 2200.00, 1, -12),
        ("Молоко", 38.50, 0, -1),
        ("Хліб", 18.00, 0, 0),
        ("Газ", 500.00, 4, -5),
        ("Вода", 150.00, 4, -2),
        ("Подарунок", 2000.00, 2, -4)
    ]

    for title, amount, cat_idx, day_offset in expenses_data:
        new_expense = Expense(
            title=title,
            amount=amount,
            category=categories[cat_idx],
            date=today + timedelta(days=day_offset),
            currency="UAH",
            description="Тестовий запис"
        )
        session.add(new_expense)

    session.commit()
    print(f"Успішно додано: {len(categories)} категорій та {len(expenses_data)} витрат!")
    session.close()

if __name__ == "__main__":
    seed_data()