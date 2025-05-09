from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import BookModel
from schemas import Book, BookCreate
from fastapi.security import OAuth2PasswordBearer

main = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_book_by_id(book_id: int, db: Session):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@main.get("/books", response_model=list[Book])
async def get_books(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    books = db.query(BookModel).all()
    return books


@main.post("/books", response_model=Book, status_code=201)
async def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_book = BookModel(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@main.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_book_by_id(book_id, db)


@main.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    book = get_book_by_id(book_id, db)
    db.delete(book)
    db.commit()
    return {}
