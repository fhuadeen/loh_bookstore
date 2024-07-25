from typing import Dict, List, Any
import os
import sys
from datetime import datetime, timezone, timedelta
import abc

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from loh_utils.loh_base import LoHBase
from loh_utils.databases.sql import Book

from flask import jsonify
from flask_restful import abort


class Inventory(LoHBase):
    def update_product(self):
        pass

    @abc.abstractmethod
    def create_products(self, products: List[Dict]):
        pass

    def delete_product(self):
        pass


class BooksInventory(Inventory):
    def get_books(self):
        kwargs = {"model_class": Book}
        books: List[Book] = self.db.query(**kwargs)

        books_list = []
        for book in books:
            books_list.append({
                'id': book.id,
                'name': book.name,
                'unit_price': book.unit_price,
                'units': book.units,
                'created_at': book.created_at.isoformat(),
            })
        return jsonify(books_list), 200

    def get_book_by_id(self, book_id: str):
        try:
            book: Book = self.db.query(model_class=Book, record_id=book_id)
        except Exception as err:
            abort(500, message=f"Failed to query db: {str(err)}")

        if not book:
            abort(404, message="Book not found")

        return jsonify({
            'id': book.id,
            'name': book.name,
            'unit_price': book.unit_price,
            'units': book.units,
            'created_at': book.created_at.isoformat(),
        }), 200

    def create_products(self, products: List[Dict]):
        
        books = []
        for product in products:
            book = Book(
                name=product.get("name"),
                unit_price=product.get("unit_price"),
                unit_cost=product.get("unit_cost"),
                units=product.get("units"),
            )
            books.append(book)

        try:
            res = [self.db.insert(book) for book in books]
        except Exception as err:
            raise Exception(f"Failed to create books in db: {str(err)}")
            # abort(500, message=f"Failed to create books in db: {str(err)}")
        return "Books created successfully"
        # return jsonify({"message": "Books created successfully"}), 201