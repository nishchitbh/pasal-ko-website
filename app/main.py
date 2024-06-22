from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from .database import engine
import psycopg2
from . import models
from .routers import products, users, auth, vote

# Creates all the tables defined by the models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Connect to the database 
try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="hello",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as err:
    print(f"Connection to the database failed.\nError: {err}")

# Includes the routers for products, users and authentication.
app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
