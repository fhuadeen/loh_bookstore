from typing import Dict, List, Any, Tuple, Optional
import os
import sys
import abc
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from loh_utils.loh_base import LoHBase
from loh_utils.databases.sql import Book
from loh_utils.media import Media

from flask import jsonify
from werkzeug.utils import secure_filename

from api.config import db, s3_obj, AI_QUEUE
from api.events import publish


class Inventory(LoHBase):
    def update_products(self):
        pass

    @abc.abstractmethod
    def create_products(self, products: List[Dict]):
        pass

    def delete_product(self):
        pass


class BooksInventory(Inventory):
    def get_books(self) -> Tuple[List[Dict], int]:
        """
        Get all books in the db.

        Returns:
            Tuple[Dict]: list of book objects
        """
        db_kwargs = {
            "model_class": [Book],
            "filters": [],
            "fetch_all": True,
        }

        books: List[Book] = self.db.query(**db_kwargs)

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

    def get_book_by_id(self, book_id: str) -> Tuple[Dict, int]:
        """
        Gets a book by the id given

        Args:
            book_id (str): Book ID

        Returns:
            Tuple[Dict, int]: Book object
        """
        try:
            db_kwargs = {
                "model_class": [Book],
                "filters": [Book.id == book_id],
                "fetch_all": False,
            }
            book: Book = self.db.query(**db_kwargs)
            print("book", book)
        except Exception as err:
            return jsonify({"error": f"Failed to query db: {str(err)}"}), 500

        if not book:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({
            'id': book.id,
            'name': book.name,
            'unit_price': book.unit_price,
            'units': book.units,
            'created_at': book.created_at.isoformat(),
        }), 200

    def create_book(
        self,
        product: Dict,
        book_file: Optional[Any] = None,
        media_obj: Media = s3_obj,
    ) -> str:


        if book_file:
            filename = secure_filename(book_file.filename)
            # print(filename)
            try:
                media_obj.upload_file(book_file, filename)
            except Exception as err:
                return jsonify({"error": f"Unable to save file to storage: {str(err)}"})
        else:
            return jsonify({"message": "File type not allowed"}, 400)

        book = Book(
            name=product.get("name"),
            file_name=filename,
            unit_price=product.get("unit_price"),
            unit_cost=product.get("unit_cost"),
            units=product.get("units"),
        )

        try:
            self.db.insert(book)
        except Exception as err:
            return jsonify({"message": f"Failed to insert in db: {str(err)}"}), 500

        # send message to inventory to update items units
        publish(
            msg=dict(book),
            queue_name=AI_QUEUE,
        )

        return jsonify({"message": "Book created successfully"}), 201

    def create_products(self, products: List[Dict]) -> str:

        books = []
        for product in products:
            book = Book(
                name=product.get("name"),
                filename=None,
                unit_price=product.get("unit_price"),
                unit_cost=product.get("unit_cost"),
                units=product.get("units"),
            )
            books.append(book)

        try:
            res = [self.db.insert(book) for book in books]
        except Exception as err:
            raise Exception(f"Failed to create books in db: {str(err)}")
        return "Books created successfully"

    @staticmethod
    def update_products_units(products: Dict) -> None:
        """
        Updates products (books) units in db.

        Args:
            products (Dict): Product IDs and value to subtract from the units left in db.

        Raises:
            Exception: Failed to update books in db
        """
        products = json.loads(products)
        for product_id, sub_value in products.items():
            update_data = {"units": Book.units - sub_value}
            try:
                db.update(
                    model_class=Book,
                    update_data=update_data,
                    record_id=product_id,
                )
            except Exception as err:
                raise Exception(f"Failed to update books in db: {str(err)}")
