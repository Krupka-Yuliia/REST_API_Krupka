from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId


class Book(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    title: str = Field(max_length=200)
    author: str = Field(max_length=200)
    publisher: str = Field(max_length=200)
    year: int = Field(gt=1500, le=datetime.now().year)

    class Config:
        json_encoders = {PydanticObjectId: str}
        allow_population_by_field_name = True
