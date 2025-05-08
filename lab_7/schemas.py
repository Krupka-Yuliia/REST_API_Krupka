from datetime import datetime
from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    title: str = Field(max_length=200)
    author: str = Field(max_length=200)
    publisher: str = Field(max_length=200)
    year: int = Field(gt=1500, le=datetime.now().year)

    class Config:
        orm_mode = True

class Book(BookCreate):
    id: int
