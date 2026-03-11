from fastapi.testclient import TestClient
from app.main import app
import os
import pytest 

client = TestClient(app)

API_KEY = os.getenv("API_KEY")
HEADERS = {"Authorization": API_KEY}

# ----- Test Books -----

def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_book():
    response = client.post("/books/", json={
        "title": "Test Book",
        "average_rating": 4.67,
        "ratings_count": 100,
        "author_ids": [],
        "category_ids": []
    }, headers = HEADERS)    

    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"

def test_get_book():
    create = client.post("/books/", json={
        "title": "Get Test Book",
        "average_rating": 3.5,
        "ratings_count": 50,
        "author_ids": [],
        "category_ids": []
    }, headers = HEADERS)
    book_id = create.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id

def test_get_book_not_found():
    response = client.get("/books/999999")
    assert response.status_code == 404

def test_update_book():
    create = client.post("/books/", json={
        "title": "Update Test Book",
        "average_rating": 2.0,
        "ratings_count": 10,
        "author_ids": [],
        "category_ids": []
    }, headers = HEADERS)
    print(create.json())
    book_id = create.json()["id"]

    response = client.patch(f"/books/{book_id}", json={
        "title": "Updated Title"
    }, headers = HEADERS)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"    

def test_delete_book():
    create = client.post("/books/", json={
        "title": "Delete Test Book",
        "average_rating": 1.0,
        "ratings_count": 5,
        "author_ids": [],
        "category_ids": []
    }, headers = HEADERS)
    book_id = create.json()["id"]

    response = client.delete(f"/books/{book_id}", headers=HEADERS)
    assert response.status_code == 204

def test_create_book_no_api_key():
    response = client.post("/books/", json={
        "title": "Unauthorized Book",
        "author_ids": [],
        "category_ids": []
    })
    assert response.status_code == 401

def test_top_rated_books():
    response = client.get("/books/top-rated/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_most_popular_books():
    response = client.get("/books/most-popular/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_books():
    response = client.get("/books/search/?keyword=test")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_books_by_author():
    author = client.post("/authors/", json={"name": "Test Author"}, headers = HEADERS)
    author_id = author.json()["id"]

    client.post("/books/", json={
        "title": "Author Test Book",
        "average_rating": 4.0,
        "ratings_count": 100,
        "author_ids": [author_id],
        "category_ids": []
    }, headers = HEADERS)

    response = client.get(f"books/filter/author/{author_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0     


# ----- Test Authors -----
 
def test_create_author():
    response = client.post("/authors/", json={"name": "Test Author 2"}, headers = HEADERS)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Author 2"                        

def test_get_authors():
    response = client.get("/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_author_not_found():
    response = client.get("/authors/999999")
    assert response.status_code == 404        