from typing import List, Dict
import os
import sys
import abc
import uuid

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from loh_utils.loh_base import LoHBase
from loh_utils.databases.sql import Order

from flask import jsonify
from flask_restful import abort

from api.config import PAYMENT_BASE_URL
from api.utils import send_post_request


class OMS(LoHBase):

    @abc.abstractmethod
    def get_orders(self, user_id: str):
        pass

    @abc.abstractmethod
    def get_order_by_id(self, order_id: str):
        pass

    def update_order(self):
        pass

    def initiate_payment(self, data: Dict):
        return send_post_request(
            url=PAYMENT_BASE_URL,
            payload=data,
        )

    def place_order(self, data: Dict):
        # user_id, items
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID not provided."}), 422
        items: List[Dict] = data.get("items")

        # TODO: Confirm quantity of books left before continuing

        # calculate total from products
        item_units = {}
        amounts = []
        for item in items:
            total = item.get('unit_price') * item.get('units_ordered')
            amounts.append(total)

            # to update inventory
            item_units[item.get('id')] = item.get('units_ordered')
        total_amount = sum(amounts)

        # create order object with order_status as pending
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            items=items,
            total_price=total_amount,
            order_status="pending",
        )

        # initiate payment
        payment_payload = {
            "user_id": user_id,
            "order_id": order.id,
            "amount": order.total_price,
        }
        try:
            res = self.initiate_payment(payment_payload)
        except Exception as err:
            return jsonify({"error": f"Error confirming payment: {err}"}), 500

        if res.status_code != 201:
            order.order_status = "failed"
            self.db.insert(order)
            return jsonify({"error": "Payment failed"}), 402

        # if paid, update order_status
        order.order_status = "confirmed"

        # save order in db
        self.db.insert(order)

        # send message to inventory to update items units
        return jsonify({"message": "Order confirmed"})


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
            'items': order.items,
            'price': order.price,
            'order_status': order.order_status,
            'created_at': order.created_at.isoformat(),
        }), 200
