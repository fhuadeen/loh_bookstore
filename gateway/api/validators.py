from typing import Optional, Dict, List, Union, Any
import abc
import html

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


class SummariseBookValidator(BaseModel):
    query: str = Field(...)


def validate(validator_class: Union[BaseModel, Any], data: Dict) -> Dict:
    """
    Runs a validator class on given payload

    Args:
        validator_class Union[BaseModel, Any]: a validator class. e.g. SignUpValidator
        data (Dict): _description_

    Raises:
        Exception: invalid payload

    Returns:
        Dict: Validated data
    """

    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Remove leading and trailing whitespace
            value = value.strip()
            # Escape HTML
            value = html.escape(value)
        sanitized_data[key] = value

    try:
        validated_data = validator_class(**sanitized_data)
    except ValidationError as err:
        raise Exception(str(err.errors()))
    return dict(validated_data)
