from database import Base
import sqlalchemy
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    password = sqlalchemy.Column(sqlalchemy.Text)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_staff = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"{self.username}"


class Order(Base):
    ORDER_STATUS = [
        ("PENDING", "pending"),
        ("IN_PROGRESS", "in_progress"),
        ("COMPLETED", "completed"),
        ("CANCELLED", "cancelled")
    ]

    PIZZA_SIZE = [
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large")
    ]

    __tablename__ = "orders"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    order_status = sqlalchemy.Column(
        ChoiceType(ORDER_STATUS), default="PENDING")
    pizza_size = sqlalchemy.Column(ChoiceType(PIZZA_SIZE), default="MEDIUM")
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"Order {self.id}, {self.quantity}, {self.order_status}, {self.pizza_size}"
