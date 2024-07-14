from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
import databases
import sqlalchemy
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
import sqlalchemy
import uuid
from model.models import User, Food, Cart, Checkout, Delivery
from model.database import UserDB, FoodDB, CartDB, CheckoutDB, DeliveryDB,Base

app = FastAPI()

DATABASE_URL = "sqlite:///./dominah.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Endpoints
@app.post("/users/", response_model=User)
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(id=user.id or uuid.uuid4(), first_name=user.first_name, email=user.email, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.first_name = user.first_name
    db_user.email = user.email
    db_user.last_name = user.last_name
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# Food Endpoints
@app.post("/foods/", response_model=Food)
async def create_food(food: Food, db: Session = Depends(get_db)):
    db_food = FoodDB(id=food.id or uuid.uuid4(), name=food.name, description=food.description, price=food.price, image_url=food.image_url)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@app.get("/foods/{food_id}", response_model=Food)
async def read_food(food_id: UUID, db: Session = Depends(get_db)):
    db_food = db.query(FoodDB).filter(FoodDB.id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return db_food

@app.put("/foods/{food_id}", response_model=Food)
async def update_food(food_id: UUID, food: Food, db: Session = Depends(get_db)):
    db_food = db.query(FoodDB).filter(FoodDB.id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    db_food.name = food.name
    db_food.description = food.description
    db_food.price = food.price
    db_food.image_url = food.image_url
    db.commit()
    db.refresh(db_food)
    return db_food

@app.delete("/foods/{food_id}", response_model=Food)
async def delete_food(food_id: UUID, db: Session = Depends(get_db)):
    db_food = db.query(FoodDB).filter(FoodDB.id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    db.delete(db_food)
    db.commit()
    return db_food

@app.get("/foods/", response_model=List[Food])
async def list_foods(db: Session = Depends(get_db)):
    db_foods = db.query(FoodDB).all()
    return db_foods


# Cart Endpoints
@app.post("/carts/", response_model=Cart)
async def create_cart(cart: Cart, db: Session = Depends(get_db)):
    food_items_str = ",".join(str(item) for item in cart.food_items)
    db_cart = CartDB(id=cart.id or uuid.uuid4(), user_id=cart.user_id, food_items=food_items_str)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@app.get("/carts/{cart_id}", response_model=Cart)
async def read_cart(cart_id: UUID, db: Session = Depends(get_db)):
    db_cart = db.query(CartDB).filter(CartDB.id == cart_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_cart.food_items = list(map(UUID, db_cart.food_items.split(",")))
    return db_cart

@app.put("/carts/{cart_id}", response_model=Cart)
async def update_cart(cart_id: UUID, cart: Cart, db: Session = Depends(get_db)):
    db_cart = db.query(CartDB).filter(CartDB.id == cart_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_cart.user_id = cart.user_id
    db_cart.food_items = ",".join(str(item) for item in cart.food_items)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@app.delete("/carts/{cart_id}", response_model=Cart)
async def delete_cart(cart_id: UUID, db: Session = Depends(get_db)):
    db_cart = db.query(CartDB).filter(CartDB.id == cart_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(db_cart)
    db.commit()
    return db_cart

# Checkout Endpoints
@app.post("/checkouts/", response_model=Checkout)
async def create_checkout(checkout: Checkout, db: Session = Depends(get_db)):
    db_checkout = CheckoutDB(id=checkout.id or uuid.uuid4(), user_id=checkout.user_id, cart_id=checkout.cart_id,
                             total_price=checkout.total_price, date=checkout.date)
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout

@app.get("/checkouts/{checkout_id}", response_model=Checkout)
async def read_checkout(checkout_id: UUID, db: Session = Depends(get_db)):
    db_checkout = db.query(CheckoutDB).filter(CheckoutDB.id == checkout_id).first()
    if db_checkout is None:
        raise HTTPException(status_code=404, detail="Checkout not found")
    return db_checkout

@app.put("/checkouts/{checkout_id}", response_model=Checkout)
async def update_checkout(checkout_id: UUID, checkout: Checkout, db: Session = Depends(get_db)):
    db_checkout = db.query(CheckoutDB).filter(CheckoutDB.id == checkout_id).first()
    if db_checkout is None:
        raise HTTPException(status_code=404, detail="Checkout not found")
    db_checkout.user_id = checkout.user_id
    db_checkout.cart_id = checkout.cart_id
    db_checkout.total_price = checkout.total_price
    db_checkout.date = checkout.date
    db.commit()
    db.refresh(db_checkout)
    return db_checkout

@app.delete("/checkouts/{checkout_id}", response_model=Checkout)
async def delete_checkout(checkout_id: UUID, db: Session = Depends(get_db)):
    db_checkout = db.query(CheckoutDB).filter(CheckoutDB.id == checkout_id).first()
    if db_checkout is None:
        raise HTTPException(status_code=404, detail="Checkout not found")
    db.delete(db_checkout)
    db.commit()
    return db_checkout

# Delivery Endpoints
@app.post("/deliveries/", response_model=Delivery)
async def create_delivery(delivery: Delivery, db: Session = Depends(get_db)):
    db_delivery = DeliveryDB(id=delivery.id or uuid.uuid4(), checkout_id=delivery.checkout_id, address=delivery.address,
                             delivery_date=delivery.delivery_date, status=delivery.status)
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@app.get("/deliveries/{delivery_id}", response_model=Delivery)
async def read_delivery(delivery_id: UUID, db: Session = Depends(get_db)):
    db_delivery = db.query(DeliveryDB).filter(DeliveryDB.id == delivery_id).first()
    if db_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return db_delivery

@app.put("/deliveries/{delivery_id}", response_model=Delivery)
async def update_delivery(delivery_id: UUID, delivery: Delivery, db: Session = Depends(get_db)):
    db_delivery = db.query(DeliveryDB).filter(DeliveryDB.id == delivery_id).first()
    if db_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db_delivery.checkout_id = delivery.checkout_id
    db_delivery.address = delivery.address
    db_delivery.delivery_date = delivery.delivery_date
    db_delivery.status = delivery.status
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@app.delete("/deliveries/{delivery_id}", response_model=Delivery)
async def delete_delivery(delivery_id: UUID, db: Session = Depends(get_db)):
    db_delivery = db.query(DeliveryDB).filter(DeliveryDB.id == delivery_id).first()
    if db_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(db_delivery)
    db.commit()
    return db_delivery
