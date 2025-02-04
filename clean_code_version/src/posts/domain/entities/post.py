from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: Optional[bool] = None

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner_username: str
    votes: int = 0
    
    class Config:
        from_attributes = True
