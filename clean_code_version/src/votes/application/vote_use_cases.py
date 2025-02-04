from ..domain.entities.vote import Vote, VoteCreate
from ..domain.services.vote_service import VoteService
from ....auth.domain.entities.user import User
from fastapi import HTTPException, status

class VoteUseCases:
    def __init__(self, vote_service: VoteService):
        self.vote_service = vote_service
    
    def vote_post(self, vote: VoteCreate, current_user: User) -> Vote:
        if vote.dir not in [0, 1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vote direction must be 0 or 1"
            )
            
        result = self.vote_service.vote_post(vote, current_user)
        
        if result is None and vote.dir == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}"
            )
        elif result is None and vote.dir == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist"
            )
            
        return result
