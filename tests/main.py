from fastapi import FastAPI
from app.routes import user_routes, book_routes, borrow_routes

app = FastAPI(title="E-Library API System")

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(book_routes.router, prefix="/books", tags=["Books"])
app.include_router(borrow_routes.router, prefix="/borrows", tags=["Borrows"])

