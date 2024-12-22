from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool = True

class Book(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool = True

class BorrowRecord(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: date
    return_date: Optional[date] = None

