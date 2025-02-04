from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ....shared.infrastructure.database import Base
from ....auth.infrastructure.models import UserModel

class PostModel(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    votes = Column(Integer, server_default='0', nullable=False)
    
    owner = relationship("UserModel", back_populates="posts")
