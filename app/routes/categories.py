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

@router.post("/", response_model=schemas.CategoryRead, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session=Depends(get_db)):
    return crud.create_category(db.category)

@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: int, db: Session=Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[schemas.CategoryRead])
def get_categories(skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=500), db: Session=Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

@router.patch("/{category_id}", response_model=schemas.CategoryRead)
def update_category(category_id: int, category_data: schemas.CategoryUpdate, db: Session=Depends(get_db)):
    category = crud.update_category(db, category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session=Depends(get_db)):
    category = delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found") 