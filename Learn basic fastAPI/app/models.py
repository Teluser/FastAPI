from database import Base
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, ForeignKey # type: ignore
import datetime 



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    rating = Column(Integer, default=0)
    created_at = Column(TIMESTAMP,  default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id", on_delete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP,  default=datetime.datetime.utcnow)