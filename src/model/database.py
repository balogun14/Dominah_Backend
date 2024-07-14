from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
import uuid

DATABASE_URL = "sqlite:///./dominah.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)


class FoodDB(Base):
    __tablename__ = "foods"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String, nullable=False)

class CartDB(Base):
    __tablename__ = "carts"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("UserDB")
    food_items = Column(String)  # Store as a comma-separated string of food item IDs

class CheckoutDB(Base):
    __tablename__ = "checkouts"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("users.id"))
    cart_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("carts.id"))
    total_price = Column(Float)
    date = Column(DateTime)

class DeliveryDB(Base):
    __tablename__ = "deliveries"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checkout_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("checkouts.id"))
    address = Column(String)
    delivery_date = Column(DateTime)
    status = Column(String)
