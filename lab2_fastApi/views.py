import uuid
from fastapi import APIRouter, HTTPException
from typing import List, Dict

from schemas import Book

main = APIRouter()

books: List[Dict] = [
    {
        "id": str(uuid.uuid4()),
        "title": "Cruel Prince",
        "author": "Holly Black",
        "publisher": "Vivat",
        "year": 2020
    },
    {
        "id": str(uuid.uuid4()),
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publisher": "Little, Brown and Company",
        "year": 1951
    }
]


async def get_book_by_id(book_id: str) -> Dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@main.get("/")
async def root():
    return {"message": "Root route"}


@main.get("/books", response_model=List[Book])
async def get_books():
    return books


@main.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    result = await get_book_by_id(book_id)
    return result


@main.post("/books", response_model=Book, status_code=201)
async def create_book(book: Book):
    try:
        book = book.model_dump()
        books.append(book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return book


@main.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str):
    book = await get_book_by_id(book_id)
    books.remove(book)
    return {}
