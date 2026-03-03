from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    category = Column(Text)
    tags = Column(Text)
    description = Column(Text)

class DetailUsageRule(Base):
    __tablename__ = "detail_usage_rules"

    id = Column(Integer, primary_key=True)
    detail_id = Column(Integer, ForeignKey("details.id"))
    host_element = Column(Text)
    adjacent_element = Column(Text)
    exposure = Column(Text)
