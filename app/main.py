from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import psycopg2
from .routers import products, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = ["localhost:5000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
