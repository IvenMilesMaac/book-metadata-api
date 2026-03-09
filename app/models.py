from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Simple association tables to connect many-to-many relationships
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True)
)

book_category = Table(
    "book_category",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True)
)

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    average_rating = Column(Float, nullable=True)
    ratings_count = Column(Integer, nullable=True)

    # Relationships
    authors = relationship("Author", secondary=book_author, back_populates="books")
    categories = relationship("Category", secondary=book_category, back_populates="books")

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    
    # Relationship to Books
    books = relationship("Book", secondary=book_author, back_populates="authors")

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    # Relationship to Books
    books = relationship("Book", secondary=book_category, back_populates="categories")