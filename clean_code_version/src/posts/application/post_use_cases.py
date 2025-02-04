from typing import List
from ..domain.entities.post import Post, PostCreate, PostUpdate
from ..domain.services.post_service import PostService
from ....auth.domain.entities.user import User
from fastapi import HTTPException, status

class PostUseCases:
    def __init__(self, post_service: PostService):
        self.post_service = post_service
    
    def create_post(self, post: PostCreate, current_user: User) -> Post:
        return self.post_service.create_post(post, current_user)
    
    def get_post(self, post_id: int) -> Post:
        post = self.post_service.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
        return post
    
    def get_posts(self, skip: int = 0, limit: int = 10) -> List[Post]:
        return self.post_service.get_posts(skip, limit)
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        return self.post_service.get_user_posts(user_id)
    
    def update_post(self, post_id: int, post: PostUpdate, current_user: User) -> Post:
        updated_post = self.post_service.update_post(post_id, post, current_user)
        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
        return updated_post
    
    def delete_post(self, post_id: int, current_user: User) -> None:
        if not self.post_service.delete_post(post_id, current_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
    
    def update_post_votes(self, post_id: int, vote_count: int) -> Post:
        updated_post = self.post_service.update_post_votes(post_id, vote_count)
        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
        return updated_post
