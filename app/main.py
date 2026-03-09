from fastapi import FastAPI
from .database import engine
from . import models
from .routes import books

app = FastAPI(title="Book Metadata API")

models.Base.metadata.create_all(bind=engine)

app.include_router(books.router) # routes here

@app.get("/")
def root():
    return {"message": "Welcome to the Book Metadata API!"}