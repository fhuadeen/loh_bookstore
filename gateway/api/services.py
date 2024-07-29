import json
from typing import Dict, List, Tuple
import os
import sys
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from loh_utils.loh_base import LoHBase
from loh_utils.databases.sql import User

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity


class Auth(LoHBase):

    def signup(self, data: Dict) -> Tuple[Dict, int]:
        """To register new user on the app"""

        # Validate input data
        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            return jsonify({"error": "Email, username, and password are required"}), 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # check if email already exists
        db_kwargs = {
            "model_class": [User],
            "filters": [User.email == data.get('email')],
            "fetch_all": False,
        }

        try:
            db_user: User = self.db.query(**db_kwargs)
        except Exception as err:
            return jsonify({"error": f"Server error: {str(err)}"}), 500
        if db_user:
            return jsonify({"error": "Email already exist"}), 400

        # check if username already exists
        try:
            db_kwargs = {
                "model_class": [User],
                "filters": [User.username == data.get('username')],
                "fetch_all": False,
            }
            db_user: User = self.db.query(**db_kwargs)
        except Exception as err:
            return jsonify({"error": f"Server error: {str(err)}"}), 500

        if db_user:
            return jsonify({"error": "Username already exist"}), 400

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
            return jsonify({"error": f"Failed to create user: {str(err)}"}), 500

        return jsonify({'id': user_obj.id, 'message': 'User created successfully'}), 201

    def login(self, data: Dict) -> Tuple[Dict, int]:
        """ Login user"""
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"error": "Username or password are required"}), 400

        try:
            db_kwargs = {
                "model_class": [User],
                "filters": [User.username == data.get('username')],
                "fetch_all": False,
            }
            user: User = self.db.query(**db_kwargs)
        except Exception as err:
            return jsonify({"error": f"Failed to query db: {str(err)}"}), 500

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401

        # Create JWT token
        access_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1))

        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200

    def get_current_user(self) -> Tuple[Dict, int]:
        """Get currently signed in user"""
        current_user_username = get_jwt_identity()
        try:
            db_kwargs = {
                "model_class": [User],
                "filters": [User.username == current_user_username],
                "fetch_all": False,
            }
            current_user: User = self.db.query(**db_kwargs)
        except Exception as err:
            return jsonify({"error": f"Failed to query db: {str(err)}"}), 500

        if not current_user:
            return jsonify({"error": "User not found"}), 404

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
