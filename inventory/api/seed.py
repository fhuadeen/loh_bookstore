from faker import Faker
import random
from typing import List

from loh_utils.databases.sql import Book

from services import BooksInventory

def generate_fake_books(num_books: int) -> List[Book]:
    """
    Geneerates fake book records.

    Args:
        num_books (int): Number of books to generate

    Returns:
        List[Book]: List of Book instances
    """
    fake = Faker()
    books = []

    for _ in range(num_books):
        book = {
            "name": fake.catch_phrase(),
            "unit_price": round(random.uniform(2000.0, 5000.0), 2),  # Random price between N2000 and N5000
            "unit_cost": round(random.uniform(1000.0, 1500.0), 2),   # Random cost between N1000 and N1500
            "units": random.randint(1, 1000)                    # Random number of units between 1 and 1000
        }
        books.append(book)

    return books

def seed_books_to_db(num_books: int, book_model_obj: BooksInventory) -> str:
    """
    Seed books into database.

    Args:
        num_books (int): Number of books to seed
        book_model_obj (BooksInventory): BooksInventory instance

    Returns:
        str: Seeded {num_books} books to db
    """

    # seed data if not exist
    # kwargs = {"model_class": Book}

    db_kwargs = {
        "model_class": [Book],
        "filters": [],
        "fetch_all": True,
    }
    db_books = book_model_obj.db.query(**db_kwargs)

    if not db_books:
        books = generate_fake_books(num_books)
        book_model_obj.create_products(books)
        print(f"Seeded {num_books} books to db")
        return f"Seeded {num_books} books to db"
