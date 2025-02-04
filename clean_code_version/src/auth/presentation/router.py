from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ...shared.infrastructure.database import get_db
from ..domain.entities.user import User, UserCreate
from ..domain.services.auth_service import AuthService
from ..infrastructure.user_repository_impl import SQLAlchemyUserRepository
from ..application.auth_use_cases import AuthUseCases

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> User:
    auth_service = AuthService(SQLAlchemyUserRepository(db, None))
    user = auth_service.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(None)
    user_repository = SQLAlchemyUserRepository(db, auth_service)
    auth_use_cases = AuthUseCases(user_repository, auth_service)
    return auth_use_cases.register_user(user)

@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    auth_service = AuthService(None)
    user_repository = SQLAlchemyUserRepository(db, auth_service)
    auth_use_cases = AuthUseCases(user_repository, auth_service)
    
    user = auth_use_cases.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_use_cases.create_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
