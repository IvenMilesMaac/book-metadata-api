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

user_favorites = Table(
    "user_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True)
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
    ratings = relationship("Ratings", back_populates="book", cascade="all, delete-orphan")
    favorited_by = relationship("User", secondary="user_favorites", back_populates="favorites")

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

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    #Relationships
    ratings = relationship("Ratings", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Book", secondary="user_favorites", back_populates="favorited_by")

# Association table with extra information
class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    rating = Column(Float, nullable=False)

    # Relationships
    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")