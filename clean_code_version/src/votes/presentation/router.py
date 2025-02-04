from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ...shared.infrastructure.database import get_db
from ...auth.presentation.router import get_current_user
from ..domain.entities.vote import Vote, VoteCreate
from ..domain.services.vote_service import VoteService
from ..infrastructure.vote_repository_impl import SQLAlchemyVoteRepository
from ..application.vote_use_cases import VoteUseCases
from ...auth.domain.entities.user import User
from ...posts.domain.services.post_service import PostService
from ...posts.infrastructure.post_repository_impl import SQLAlchemyPostRepository

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

def get_vote_use_cases(db: Session = Depends(get_db)) -> VoteUseCases:
    vote_repository = SQLAlchemyVoteRepository(db)
    post_repository = SQLAlchemyPostRepository(db)
    post_service = PostService(post_repository)
    vote_service = VoteService(vote_repository, post_service)
    return VoteUseCases(vote_service)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteCreate,
    current_user: User = Depends(get_current_user),
    vote_use_cases: VoteUseCases = Depends(get_vote_use_cases)
):
    return vote_use_cases.vote_post(vote, current_user)
