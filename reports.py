from sqlalchemy import func
from datetime import date
from models import Expense, Category


# Фільтрація витрат за датою, назвою, категорією.
def filter_expenses(session, start_date=None, end_date=None, title=None, category_name=None):
    query = session.query(Expense).join(Category)

    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    if title:
        query = query.filter(Expense.title.ilike(f"%{title}%"))
    if category_name:
        query = query.filter(Category.name.ilike(f"%{category_name}%"))

    return query.all()

# Максимальна витрата у кожній категорії.
def get_max_expense_per_category(session):
    return (
        session.query(Category.name, func.max(Expense.amount))
        .join(Expense)
        .group_by(Category.id, Category.name)
        .all()
    )

# Максимальна витрата у періоді.
def get_max_expense_in_period(session, start_date, end_date, mode="max"):
    return session.query(func.max(Expense.amount)) \
        .filter(Expense.date.between(start_date, end_date)) \
        .scalar()

# Мінімальна витрата у кожній категорії.
def get_min_expense_per_category(session):
    return (
        session.query(Category.name, func.min(Expense.amount))
        .join(Expense)
        .group_by(Category.id, Category.name)
        .all()
    )

# Мінімальна витрата у періоді
def get_min_expense_in_period(session, start_date, end_date):
    return (
        session.query(func.min(Expense.amount))
        .filter(Expense.date >= start_date)
        .filter(Expense.date <= end_date)
        .scalar()
    )

# Підсумки по категоріях (Сума по кожній)
def get_totals_by_category(session):
    return session.query(Category.name, func.sum(Expense.amount)) \
        .join(Expense) \
        .group_by(Category.id).all()


# ТОП категорія
def get_top_category(session):
    return session.query(Category.name, func.sum(Expense.amount)) \
        .join(Expense) \
        .group_by(Category.id) \
        .order_by(func.sum(Expense.amount).desc()).first()


# Середні витрати на день за період
def get_daily_average_in_period(session, start_date, end_date):
    total_sum = session.query(func.sum(Expense.amount)) \
                    .filter(Expense.date.between(start_date, end_date)) \
                    .scalar() or 0

    days_count = (end_date - start_date).days + 1
    return total_sum / days_count if days_count > 0 else 0