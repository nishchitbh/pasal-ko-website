from typing import Optional
from ..entities.vote import Vote, VoteCreate
from ..repositories.vote_repository import VoteRepository
from ....auth.domain.entities.user import User
from ....posts.domain.services.post_service import PostService

class VoteService:
    def __init__(self, vote_repository: VoteRepository, post_service: PostService):
        self.vote_repository = vote_repository
        self.post_service = post_service
    
    def vote_post(self, vote: VoteCreate, current_user: User) -> Vote:
        # Verify post exists
        post = self.post_service.get_post(vote.post_id)
        if not post:
            return None
            
        # Check if user has already voted
        existing_vote = self.vote_repository.get_vote(vote.post_id, current_user.id)
        
        if vote.dir == 1:
            if existing_vote:
                return None  # User already voted
            new_vote = self.vote_repository.create(vote, current_user.id)
        else:
            if not existing_vote:
                return None  # No vote to delete
            self.vote_repository.delete(vote.post_id, current_user.id)
            new_vote = None
            
        # Update post vote count
        vote_count = self.vote_repository.get_vote_count(vote.post_id)
        self.post_service.update_post_votes(vote.post_id, vote_count)
        
        return new_vote
