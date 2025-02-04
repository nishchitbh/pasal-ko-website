from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.post import Post, PostCreate, PostUpdate

class PostRepository(ABC):
    @abstractmethod
    def create(self, post: PostCreate, owner_id: int) -> Post:
        pass
    
    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional[Post]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Post]:
        pass
    
    @abstractmethod
    def get_by_owner(self, owner_id: int) -> List[Post]:
        pass
    
    @abstractmethod
    def update(self, post_id: int, post: PostUpdate, owner_id: int) -> Optional[Post]:
        pass
    
    @abstractmethod
    def delete(self, post_id: int, owner_id: int) -> bool:
        pass
    
    @abstractmethod
    def update_votes(self, post_id: int, vote_count: int) -> Optional[Post]:
        pass
