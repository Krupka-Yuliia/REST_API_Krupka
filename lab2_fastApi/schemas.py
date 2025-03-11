import uuid
from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str
    author: str
    publisher: str
    year: int
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
