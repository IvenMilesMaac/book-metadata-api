from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal  

router = APIRouter(prefix="/books", tags=["Books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# ----- Basic CRUD Endpoints -----

@router.post("/", response_model=schemas.BookRead, status_code=201)
def create_book(book: schemas.BookCreate, db: Session=Depends(get_db)):
    return crud.create_book(db, book)

@router.get("/", response_model=List[schemas.BookRead])
def get_books(skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)               

@router.get("/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, db: Session=Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found") 
    return book

@router.patch("/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, book_data: schemas.BookUpdate, db: Session=Depends(get_db)):
    book = crud.update_book(db, book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session=Depends(get_db)):
    book = crud.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
# ----- Analytical Endpoints -----     