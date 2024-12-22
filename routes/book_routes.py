from fastapi import APIRouter, HTTPException
from app.models import Book
from app.database import books_db

router = APIRouter()

@router.get("/")
def get_all_books():
    return books_db

@router.post("/")
def create_book(book: Book):
    if any(b.id == book.id for b in books_db):
        raise HTTPException(status_code=400, detail="Book ID already exists")
    books_db.append(book)
    return book

@router.get("/{book_id}")
def get_book(book_id: int):
    book = next((b for b in books_db if b.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for idx, book in enumerate(books_db):
        if book.id == book_id:
            books_db[idx] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@router.post("/{book_id}/mark_unavailable")
def mark_book_unavailable(book_id: int):
    book = next((b for b in books_db if b.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.is_available = False
    return {"message": "Book marked as unavailable"}

