from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from ..domain.entities.post import Post, PostCreate, PostUpdate
from ..domain.repositories.post_repository import PostRepository
from .models import PostModel
from fastapi import HTTPException, status

class SQLAlchemyPostRepository(PostRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, post: PostCreate, owner_id: int) -> Post:
        db_post = PostModel(
            **post.dict(),
            owner_id=owner_id
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return Post.from_orm(db_post)
    
    def get_by_id(self, post_id: int) -> Optional[Post]:
        post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
        return Post.from_orm(post)
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Post]:
        posts = self.db.query(PostModel)\
            .order_by(desc(PostModel.created_at))\
            .offset(skip)\
            .limit(limit)\
            .all()
        return [Post.from_orm(post) for post in posts]
    
    def get_by_owner(self, owner_id: int) -> List[Post]:
        posts = self.db.query(PostModel)\
            .filter(PostModel.owner_id == owner_id)\
            .order_by(desc(PostModel.created_at))\
            .all()
        return [Post.from_orm(post) for post in posts]
    
    def update(self, post_id: int, post_update: PostUpdate, owner_id: int) -> Optional[Post]:
        post_query = self.db.query(PostModel).filter(PostModel.id == post_id)
        post = post_query.first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
            
        if post.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action"
            )
            
        post_query.update(post_update.dict(exclude_unset=True))
        self.db.commit()
        return Post.from_orm(post_query.first())
    
    def delete(self, post_id: int, owner_id: int) -> bool:
        post_query = self.db.query(PostModel).filter(PostModel.id == post_id)
        post = post_query.first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
            
        if post.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action"
            )
            
        post_query.delete()
        self.db.commit()
        return True
    
    def update_votes(self, post_id: int, vote_count: int) -> Optional[Post]:
        post_query = self.db.query(PostModel).filter(PostModel.id == post_id)
        post = post_query.first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {post_id} was not found"
            )
            
        post_query.update({"votes": vote_count})
        self.db.commit()
        return Post.from_orm(post_query.first())
