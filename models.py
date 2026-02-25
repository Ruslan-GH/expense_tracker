from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255))
    currency = Column(String(10), default="UAH")

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )

    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)

    category = relationship("Category", back_populates="expenses")