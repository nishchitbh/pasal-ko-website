from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ...shared.infrastructure.database import get_db
from ...auth.presentation.router import get_current_user
from ..domain.entities.post import Post, PostCreate, PostUpdate
from ..domain.services.post_service import PostService
from ..infrastructure.post_repository_impl import SQLAlchemyPostRepository
from ..application.post_use_cases import PostUseCases
from auth.domain.entities.user import User

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

def get_post_use_cases(db: Session = Depends(get_db)) -> PostUseCases:
    post_repository = SQLAlchemyPostRepository(db)
    post_service = PostService(post_repository)
    return PostUseCases(post_service)

@router.get("/", response_model=List[Post])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    post_use_cases: PostUseCases = Depends(get_post_use_cases)
):
    return post_use_cases.get_posts(skip, limit)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    post_use_cases: PostUseCases = Depends(get_post_use_cases)
):
    return post_use_cases.create_post(post, current_user)

@router.get("/{post_id}", response_model=Post)
def get_post(
    post_id: int,
    post_use_cases: PostUseCases = Depends(get_post_use_cases)
):
    return post_use_cases.get_post(post_id)

@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    post: PostUpdate,
    current_user: User = Depends(get_current_user),
    post_use_cases: PostUseCases = Depends(get_post_use_cases)
):
    return post_use_cases.update_post(post_id, post, current_user)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_use_cases: PostUseCases = Depends(get_post_use_cases)
):
    post_use_cases.delete_post(post_id, current_user)

@router.get("/user/{user_id}", response_model=List[Post])
def get_user_posts(
    user_id: int,
    post_use_cases: PostUseCases = Depends(get_post_use_cases)
):
    return post_use_cases.get_user_posts(user_id)
