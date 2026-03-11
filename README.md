# Book Metadata API

This is a RESTful API that allows the user to browse and query book metadata. It is built with FastAPI and SQLAlchemy to provide full CRUD operations for books, authors, and categories. It also has analytical endpoints for searching, filtering, and ranking books using the Goodreads dataset. 

## Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## Setup & Installation

1. Clone the repository
git clone https://github.com/IvenMilesMaac/book-metadata-api

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Set up environment variables
Create a .env file in the project root with the following:
API_KEY = 8d9a1fe6425324282d852de957b6d09dfa1373928022351034d2560f00af476f

## Running the API
uvicorn app.main:app --reload

Then go to http://127.0.0.1:8000/docs to view and interact with the API

## Authentication
Write operations (POST, PATCH, DELETE) require an API key passed in the request header as 'Authorization'.
In Swagger UI, click the Authorize button at the top of the /docs page and enter the API key before testing write endpoints.

## Populating the Database
The dataset used is the Goodreads Books dataset from Kaggle:
https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks

Download books.csv and place it in the project root, then run: 
python seed.py

Note: The Goodreads dataset does not include category data. Category endpoints are fully implemented but will return empty results unless categories are added manually via the API.

## API Documentation
See [API Documentation](___) for a full list of endpoints, parameters, and example responses.

## Deployed API
The live API is available at: https://book-metadata-api.onrender.com/