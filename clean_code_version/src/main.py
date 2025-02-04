from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth.presentation.router import router as auth_router
from .posts.presentation.router import router as posts_router
from .votes.presentation.router import router as votes_router
from .shared.infrastructure.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware configuration
origins = ["*"]  # In production, replace with specific origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(votes_router)

@app.get("/")
def root():
    return {"message": "Welcome to Pasal-ko-Website API"}
