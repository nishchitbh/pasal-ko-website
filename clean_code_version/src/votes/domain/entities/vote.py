from datetime import datetime
from pydantic import BaseModel

class VoteBase(BaseModel):
    post_id: int
    dir: int  # 1 for upvote, 0 for downvote

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
