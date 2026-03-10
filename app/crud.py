from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import desc

# ----- CRUD operations for Books -----
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title = book.title,
        average_rating = book.average_rating,
        ratings_count = book.ratings_count
    )

    # resolve and attach foreign entities 
    if book.author_ids:
        authors = db.query(models.Author).filter(models.Author.id.in_(book.author_ids)).all()
        db_book.authors = authors
    if book.category_ids:
        categories = db.query(models.Category).filter(models.Category.id.in_(book.category_ids)).all()
        db_book.categories = categories

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return book

def get_books(db: Session, skip: int=0, limit: int=100):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

def update_book(db: Session, book_id: int, book_data: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book: 
        return None
    
    # Update simple fields if provided
    if book_data.title is not None:
        db_book.title = book_data.title
    if book_data.average_rating is not None:
        db_book.average_rating = book_data.average_rating
    if book_data.ratings_count is not None:
        db_book.ratings_count = book_data.ratings_count

    # Replace foreign entities if new list provided
    if book_data.author_ids is not None:
        db_book.authors = db.query(models.Author).filter(models.Author.id.in_(book_data.author_ids).all())
    if book_data.category_ids is not None:
        db_book.category = db.query(models.Category).filter(models.Category.id.in_(book_data.category_ids).all())

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    db.delete(db_book)
    db.commit()
    return db_book


# ----- CRUD operations for Authors -----
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author

def get_authors(db: Session, skip: int=0, limit: int=100):
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors    

def update_author(db: Session, author_id: int, author_data: schemas.AuthorUpdate):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    if author_data.name is not None:
        db_author.name = author_data.name

    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    
    db.delete(db_author)
    db.commit()
    return db_author


# ----- CRUD operations for Categories -----
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Catgory.id == category_id).irst()
    return category

def get_categories(db: Session, skip: int=0, limit: int=100):
    categories = db.query(models.Category).offset(skip).limit(limit).all() 
    return categories

def update_category(db: Session, category_id: int, category_data: schemas.CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    if category_data.name is not None:
        db_category.name = category_data.name

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if not db_category:
        return None         
    
    db.delete(db_category)
    db.commit()
    return db_category


# ----- Analytical Queries -----

def get_books_by_rating(db: Session, skip: int=0, limit: int=100, min_ratings: int=0):
    return (
        db.query(models.Book)
        .filter(models.Book.average_rating.isnot(None))
        .filter(models.Book.ratings_count >= min_ratings) # make sorting by ratings meaningful
        .order_by(desc(models.Book.average_rating))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_books_by_category(db: Session, category_id: int, skip: int=0, limit: int=100):
    return (
        db.query(models.Book)
        .filter(models.Book.categories.any(models.Category.id == category_id))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_books_by_author(db: Session, author_id: int, skip: int=0, limit: int=100):
    return (
        db.query(models.Book)
        .filter(models.Book.authors.any(models.Author.id == author_id))
        .offset(skip)
        .limit(limit)
        .all()
    )

def search_books_by_title(db: Session, keyword: str, skip: int=0, limit: int=100):
    return (
        db.query(models.Book)
        .filter(models.Book.title.ilike(f"%{keyword}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_books_by_rating_count(db: Session, skip: int=0, limit: int=100):
    return (
        db.query(models.Book)
        .filter(models.Book.ratings_count.isnot(None))
        .order_by(desc(models.Book.ratings_count))
        .offset(skip)
        .limit(limit)
        .all()
    )