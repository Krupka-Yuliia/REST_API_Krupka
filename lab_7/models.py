from sqlalchemy import Column, String, Integer
from database import Base

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
