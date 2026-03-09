from fastapi import FastAPI
from .database import engine
from . import models
from .routes import books, authors, categories

app = FastAPI(title="Book Metadata API")

models.Base.metadata.create_all(bind=engine)

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Book Metadata API!"}