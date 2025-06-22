from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .core.database import Base
import uuid

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String, unique=True, nullable=False)
  password = Column(String, nullable=False)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  role = Column(String, default="user")
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  articles = relationship("Article", back_populates="author")
  comments = relationship("Comment", back_populates="user")

class Tag(Base):
  __tablename__ = "tags"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String, nullable=False)

  articles = relationship("Article", back_populates="tag")

class Article(Base):
  __tablename__ = "articles"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = Column(Integer, ForeignKey("users.id"))
  tag_id = Column(Integer, ForeignKey("tags.id"))
  title = Column(String, nullable=False)
  content = Column(Text, nullable=False)
  thumbnail = Column(String, nullable=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  author = relationship("User", back_populates="articles")
  tag = relationship("Tag", back_populates="articles")
  comments = relationship("Comment", back_populates="article")

class Comment(Base):
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"))
  user_id = Column(Integer, ForeignKey("users.id"))
  content = Column(Text, nullable=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  article = relationship("Article", back_populates="comments")
  user = relationship("User", back_populates="comments")