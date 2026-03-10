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
 
@router.delete("/top/rated", response_model=List[schemas.BookRead])
def get_top_rated_books(skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), min_ratings: int=Query(default=0, ge=0), db: Session=Depends(get_db)):
    return crud.get_books_by_rating(db, skip=skip, limit=limit, min_ratings=min_ratings)  

@router.get("/filter/category/{category_id}", response_model=List[schemas.BookRead])
def get_books_by_category(category_id: int, skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    books = crud.get_books_by_category(db, category_id=category_id, skip=skip, limit=limit)
    if books is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return books

@router.get("/filter/author/{author_id}", response_model=List[schemas.BookRead])
def get_books_by_author(author_id: int, skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    if books is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return books 

@router.get("/search/", response_model=List[schemas.BookRead])
def search_books(keyword: str=Query(..., min_length=1), skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    return crud.search_books_by_title(db, keyword=keyword, skip=skip, limit=limit)

@router.get("/most-popular/", response_model=List[schemas.BookRead])
def get_most_popular_books(skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    return crud.get_books_by_rating_count(db, skip=skip, limit=limit)