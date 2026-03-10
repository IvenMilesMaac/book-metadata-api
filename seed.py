import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal, engine
from app import models

CSV_FILE = "books.csv"
LIMIT = 1000

def seed():
    db = SessionLocal()

    author_cache = {}

    try:
        with open(CSV_FILE, newline='', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader):
                if i >= LIMIT:
                    break

                title = row.get("title", "").strip()
                if not title:
                    continue

                try:
                    average_rating = float(row.get("average_rating", "").strip()) 
                except ValueError:
                    average_rating = None

                try:
                    ratings_count = int(row.get("ratings_count", "").strip())
                except ValueError:
                    ratings_count = None

                raw_authors = row.get("authors", "").strip()
                author_objects = []

                if raw_authors:
                    author_names = [a.strip() for a in raw_authors.split("/") if a.strip()]

                    for name in author_names:
                        if name not in author_cache:
                            db_author = db.query(models.Author).filter(
                                models.Author.name == name
                            ).first()

                            if not db_author:
                                db_author = models.Author(name=name)
                                db.add(db_author)
                                db.flush()

                            author_cache[name] = db_author

                        author_objects.append(author_cache[name])

                db_book = models.Book(
                    title=title,
                    average_rating=average_rating,
                    ratings_count=ratings_count
                )
                db_book.authors = author_objects

                db.add(db_book)

            db.commit()
            print(f"Seeding complete. Imported up to {LIMIT} books.")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise

    finally:
        db.close()

if __name__ == "__main__":
    seed()                                                                                                    