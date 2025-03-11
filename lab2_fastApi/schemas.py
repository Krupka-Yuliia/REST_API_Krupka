import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(max_length=200)
    author: str = Field(max_length=200)
    publisher: str = Field(max_length=200)
    year: int = Field(gt=1500, le=datetime.now().year)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Books(BaseModel):
    books: List[Book]

