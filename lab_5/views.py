from typing import List

from fastapi import APIRouter
from pydantic_mongo import PydanticObjectId
from models import Book
from database import db
from fastapi import HTTPException

library = APIRouter()


@library.get("/")
async def root():
    return {"message": "Root route"}


@library.post("/books", response_model=Book, status_code=201)
async def create_book(book: Book):
    try:
        book_dict = book.dict(by_alias=True)
        result = await db.books.insert_one(book_dict)
        book_dict["_id"] = str(result.inserted_id)
        return book_dict
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while creating the book: {str(e)}"
        )


@library.get("/books", response_model=List[Book])
async def get_books():
    books_cursor = db.books.find({})
    books = await books_cursor.to_list(length=20)
    return books


@library.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    book = await db.books.find_one({"_id": PydanticObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@library.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str):
    response = await db.books.delete_one({"_id": PydanticObjectId(book_id)})
    if response.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return {}
