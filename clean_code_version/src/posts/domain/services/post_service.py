from typing import List, Optional
from ..entities.post import Post, PostCreate, PostUpdate
from ..repositories.post_repository import PostRepository
from ....auth.domain.entities.user import User

class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    def create_post(self, post: PostCreate, current_user: User) -> Post:
        return self.post_repository.create(post, current_user.id)
    
    def get_post(self, post_id: int) -> Optional[Post]:
        return self.post_repository.get_by_id(post_id)
    
    def get_posts(self, skip: int = 0, limit: int = 10) -> List[Post]:
        return self.post_repository.get_all(skip, limit)
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        return self.post_repository.get_by_owner(user_id)
    
    def update_post(self, post_id: int, post: PostUpdate, current_user: User) -> Optional[Post]:
        return self.post_repository.update(post_id, post, current_user.id)
    
    def delete_post(self, post_id: int, current_user: User) -> bool:
        return self.post_repository.delete(post_id, current_user.id)
    
    def update_post_votes(self, post_id: int, vote_count: int) -> Optional[Post]:
        return self.post_repository.update_votes(post_id, vote_count)
