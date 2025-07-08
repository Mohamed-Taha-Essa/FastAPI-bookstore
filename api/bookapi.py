from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.book import Book 
from schemas.book import BookResponse, BookCreate
from core.database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse)
def create_book_api(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/search", response_model=list[BookResponse])
def search_books_api(db: Session = Depends(get_db), search: str = ""):
    try:
        db_books = db.query(Book).filter(Book.title.contains(search)).all()
        if not db_books:
            try:
                db_books = db.query(Book).filter(Book.description.contains(search)).all()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return db_books


@router.get("/{book_id}", response_model=BookResponse)
def get_book_api(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/", response_model=list[BookResponse])
def list_books_api(db: Session = Depends(get_db)):
    db_books = db.query(Book).all()
    return db_books


@router.put("/{book_id}", response_model=BookResponse)
def update_book_api(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.description = book.description
    db_book.author_id = book.author_id
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", response_model=dict)
def delete_book_api(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}