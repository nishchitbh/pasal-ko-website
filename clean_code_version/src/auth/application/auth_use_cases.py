from typing import Optional
from ..domain.entities.user import User, UserCreate
from ..domain.repositories.user_repository import UserRepository
from ..domain.services.auth_service import AuthService
from fastapi import HTTPException, status

class AuthUseCases:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def register_user(self, user: UserCreate) -> User:
        if self.user_repository.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if self.user_repository.get_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        return self.user_repository.create(user)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        if not self.auth_service.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_token(self, user: User) -> str:
        access_token = self.auth_service.create_access_token(
            data={"user_id": user.id}
        )
        return access_token
