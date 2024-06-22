from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Product(Base):
    """Defines the structure of the products table"""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User")


class User(Base):
    """Defines the structure of the users table"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
    approved = Column(Boolean, nullable=False, server_default="False")
    admin = Column(Boolean, nullable=False, server_default="False")


class Votes(Base):
    """Defines the structure of the vote table"""

    __tablename__ = "votes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
