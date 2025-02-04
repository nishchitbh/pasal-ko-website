from abc import ABC, abstractmethod
from typing import Optional
from ..entities.vote import Vote, VoteCreate

class VoteRepository(ABC):
    @abstractmethod
    def create(self, vote: VoteCreate, user_id: int) -> Vote:
        pass
    
    @abstractmethod
    def get_vote(self, post_id: int, user_id: int) -> Optional[Vote]:
        pass
    
    @abstractmethod
    def delete(self, post_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_vote_count(self, post_id: int) -> int:
        pass
