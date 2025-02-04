from sqlalchemy.orm import Session
from typing import Optional
from ..domain.entities.user import User, UserCreate
from ..domain.repositories.user_repository import UserRepository
from .models import UserModel
from ..domain.services.auth_service import AuthService

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service
    
    def create(self, user: UserCreate) -> User:
        hashed_password = self.auth_service.get_password_hash(user.password)
        db_user = UserModel(
            email=user.email,
            username=user.username,
            password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User.from_orm(db_user)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return User.from_orm(user) if user else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return User.from_orm(user) if user else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return User.from_orm(user) if user else None
