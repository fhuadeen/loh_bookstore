from typing import Optional, Dict, List
import abc

from pydantic import BaseModel, EmailStr, Field, ValidationError
from flask import jsonify


class SignUpValidator(BaseModel):
    first_name: str = Field(...)
    last_name: Optional[str] = Field(default=None)
    email: EmailStr = Field(...)
    gender: Optional[str] = Field(default=None)
    username: str = Field(...)
    password: str = Field(...)
    address: Optional[str] = Field(default=None)


class LoginValidator(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class PlaceOrderValidator(BaseModel):
    items: List[Dict] = Field(...)


class UpdateOrderStatusValidator(BaseModel):
    order_id: str = Field(...)
    order_status: str = Field(...)
    user_id: str = Field(...)


def validate(validator_class, data):
    try:
        validated_data = validator_class(**data)
    except ValidationError as err:
        raise Exception(str(err.errors()))
    return dict(validated_data)
