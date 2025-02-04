from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql.expression import text
from ....shared.infrastructure.database import Base

class VoteModel(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
