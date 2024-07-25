from typing import Dict
import os
import sys
import abc
import random

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)


from flask import jsonify
from flask_restful import abort


class Payment(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def pay(self, user_id: str):
        pass


class LoHstack(Payment):
    def pay(self, data: Dict):

        # dummy payment
        res = random.choice((0,1,2,3,4,5))
        if res == 0:
            return jsonify({"error": "Payment failed. Please try again."}), 402
        return jsonify({
            "message": "Payment successful",
            "user_id": data.get("user_id"),
            "order_id": data.get("order_id"),
            "amount": data.get("amount"),
        }), 201
