from pydantic import BaseModel
from typing import Optional, List

# Author Schemas
class AuthorCreate(BaseModel):
    name: str

class AuthorUpdate(BaseModel):
    name: Optional[str] = None

class AuthorRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Category Schemas
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None    

class CategoryRead(BaseModel):
    id: int
    name: str

    class Config: 
        from_attributes = True     

# Book Schemas
class BookBase(BaseModel):
    title: str
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None

class BookCreate(BookBase):
    author_ids: List[int] = []
    category_ids: List[int] = []

class BookUpdate(BaseModel):
    title: Optional[str] = None
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None
    author_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None 

class BookRead(BookBase):
    id: int
    authors: List[AuthorRead]
    categories: List[CategoryRead]
    
    class Config:
        from_attributes = True 