from typing import Dict, List
import os
import sys
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from loh_utils.loh_base import LoHBase
from loh_utils.databases.sql import User

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_restful import abort
from flask_jwt_extended import create_access_token, get_jwt_identity


class Auth(LoHBase):

    def signup(self, data: Dict):

        # Validate input data
        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            abort(400, message="Email, username, and password are required")

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data['email'],
            gender=data.get('gender'),
            username=data['username'],
            password=hashed_password,
            address=data.get('address', ''),
            is_verified=False,
            is_admin=False,
        )

        try:
            user_obj: User = self.db.insert(new_user)
        except Exception as err:
            abort(500, message=f"Failed to create user: {str(err)}")

        return jsonify({'id': user_obj.id, 'message': 'User created successfully'}), 201

    def login(self, data: Dict):
        if not data or not data.get('username') or not data.get('password'):
            abort(400, message="Username, and password are required")

        user: User = self.db.query(username=data.get('username'))

        if not user or not check_password_hash(user.password, data['password']):
            abort(401, message=f"Invalid credentials")
            return jsonify({'message': 'Unauthorized'}), 401

        # Create JWT token
        access_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1))

        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200

    def get_current_user(self):
        current_user_username = get_jwt_identity()
        current_user: User = self.db.query(username=current_user_username)

        if not current_user:
            abort(404, message="User not found")

        return jsonify({
            'id': current_user.id,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'gender': current_user.gender,
            'username': current_user.username,
            'address': current_user.address,
        }), 200


class UserAuth(Auth):
    ...
