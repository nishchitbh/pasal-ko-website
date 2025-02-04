from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User, UserCreate

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: UserCreate) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
