from fastapi import APIRouter, HTTPException
from datetime import date
from app.models import BorrowRecord
from app.database import users_db, books_db, borrow_records_db

router = APIRouter()

@router.post("/borrow")
def borrow_book(user_id: int, book_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    book = next((b for b in books_db if b.id == book_id), None)

    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="User not active or not found")
    if not book or not book.is_available:
        raise HTTPException(status_code=400, detail="Book not available or not found")
    if any(r.user_id == user_id and r.book_id == book_id for r in borrow_records_db):
        raise HTTPException(status_code=400, detail="Book already borrowed by the user")

    record = BorrowRecord(
        id=len(borrow_records_db) + 1,
        user_id=user_id,
        book_id=book_id,
        borrow_date=date.today(),
    )
    borrow_records_db.append(record)
    book.is_available = False
    return record

@router.post("/return")
def return_book(record_id: int):
    record = next((r for r in borrow_records_db if r.id == record_id), None)
    if not record or record.return_date:
        raise HTTPException(status_code=400, detail="Invalid return request")

    book = next((b for b in books_db if b.id == record.book_id), None)
    record.return_date = date.today()
    book.is_available = True
    return {"message": "Book returned successfully"}

@router.get("/user/{user_id}")
def get_borrow_records_by_user(user_id: int):
    return [r for r in borrow_records_db if r.user_id == user_id]

@router.get("/")
def get_all_borrow_records():
    return borrow_records_db

