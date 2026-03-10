from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/authors", tags=["Authors"])

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# ----- Basic CRUD Endpoints -----

@router.post("/", response_model=schemas.AuthorRead, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session=Depends(get_db)):
    return crud.create_author(db, author)

@router.get("/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session=Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/", response_model=List[schemas.AuthorRead])
def get_authors(skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@router.patch("/{author_id}", response_model=schemas.AuthorRead)
def update_author(author_id: int, author_data: schemas.AuthorUpdate, db: Session=Depends(get_db)):
    author = crud.update_author(db, author_id, author_data)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author 

@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session=Depends(get_db)):
    author = crud.delete_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found") 