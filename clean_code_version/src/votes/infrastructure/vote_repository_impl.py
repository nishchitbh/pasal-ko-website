from sqlalchemy.orm import Session
from typing import Optional
from ..domain.entities.vote import Vote, VoteCreate
from ..domain.repositories.vote_repository import VoteRepository
from .models import VoteModel
from fastapi import HTTPException, status

class SQLAlchemyVoteRepository(VoteRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, vote: VoteCreate, user_id: int) -> Vote:
        db_vote = VoteModel(
            post_id=vote.post_id,
            user_id=user_id
        )
        self.db.add(db_vote)
        self.db.commit()
        self.db.refresh(db_vote)
        return Vote.from_orm(db_vote)
    
    def get_vote(self, post_id: int, user_id: int) -> Optional[Vote]:
        vote = self.db.query(VoteModel)\
            .filter(VoteModel.post_id == post_id, VoteModel.user_id == user_id)\
            .first()
        return Vote.from_orm(vote) if vote else None
    
    def delete(self, post_id: int, user_id: int) -> bool:
        vote_query = self.db.query(VoteModel)\
            .filter(VoteModel.post_id == post_id, VoteModel.user_id == user_id)
        vote = vote_query.first()
        
        if not vote:
            return False
            
        vote_query.delete()
        self.db.commit()
        return True
    
    def get_vote_count(self, post_id: int) -> int:
        return self.db.query(VoteModel)\
            .filter(VoteModel.post_id == post_id)\
            .count()
