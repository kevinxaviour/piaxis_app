from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True)
    email = Column(Text)
    role  = Column(Text)

class Detail(Base):
    __tablename__ = "details"

    id          = Column(Integer, primary_key=True)
    title       = Column(Text)
    category    = Column(Text)
    tags        = Column(Text)
    description = Column(Text)
    source      = Column(Text)
    owner_id    = Column(Integer, ForeignKey("users.id"), nullable=True)