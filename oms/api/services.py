from typing import Dict, List, Any
import os
import sys
from datetime import datetime, timezone, timedelta
import abc

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from loh_utils.loh_base import LoHBase
from loh_utils.databases.sql import Order, User

from flask import jsonify
from flask_restful import abort


class OMS(LoHBase):

    @abc.abstractmethod
    def get_orders(self, user_id: str):
        pass

    @abc.abstractmethod
    def get_order_by_id(self, order_id: str):
        pass

    def place_order(self):
        pass


class BookOMS(OMS):
    def get_orders(self, user_id: str):
        db_kwargs = {
            "model_class": Order,
            "filters": [Order.user_id == user_id]
        }
        try:
            orders: List[Order] = self.db.query(**db_kwargs)
        except Exception as err:
            abort(500, message=f"Failed to query db: {str(err)}")

        orders_list = []
        for order in orders:
            # return needed attributes only to reduce packet
            orders_list.append({
                'id': order.id,
                'user_id': order.user_id,
                'order_status': order.order_status,
                'created_at': order.created_at.isoformat(),
            })
        return jsonify(orders_list), 200

    def get_order_by_id(self, order_id: str, user_id: str):
        try:
            order: Order = self.db.query(model_class=Order, record_id=order_id)
        except Exception as err:
            abort(500, message=f"Failed to query db: {str(err)}")

        if not order:
            abort(404, message="Order not found")

        # if order not for current user
        if order.user_id != user_id:
            abort(404, message="Order not found")

        return jsonify({
            'id': order.id,
            'user_id': order.user_id,
            'books': order.books,
            'price': order.price,
            'order_status': order.order_status,
            'created_at': order.created_at.isoformat(),
        }), 200
