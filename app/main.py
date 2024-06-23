from fastapi import FastAPI
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
# Includes the routers for products, users and authentication.
app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
