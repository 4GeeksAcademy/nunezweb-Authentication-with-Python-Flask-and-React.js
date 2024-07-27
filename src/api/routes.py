"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from api.models import db, User, TokenBlockList
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def user_signup():
    body = request.get_json()
    if "email" not in body:
        return jsonify({"msg": "Field Required email"}), 400
    if "password" not in body:
        return jsonify({"msg": "Field Required password"}), 400
    
    encrypted_password=bcrypt.generate_password_hash(body["password"]).decode('utf-8')

    new_user = User(email=body["email"], password=encrypted_password, is_active=True)

    if "first_name" in body:
        new_user.first_name = body["first_name"]
    else:
        new_user.first_name = "" 

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201  


@api.route('/login', methods=['POST'])
def user_login():
    body=request.get_json()
    if "email" not in body:
        return jsonify({"msg": "Field Required email"}), 400
    if "password" not in body:
        return jsonify({"msg": "Field Required password"}), 400
    user=User.query.filter_by(email=body["email"]).first()
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    
    if not user.is_active:
        return jsonify({"msg": "The user is not active"}), 400

    password_check=bcrypt.check_password_hash(user.password, body["password"]) # returns True
    if password_check == False:
        return jsonify({"msg": "Password not valid"}), 401

    role = "admin"
    if user.id %2 == 0:
        role = "user"
    token = create_access_token(identity=user.id, additional_claims={"role": role})
    return jsonify({"token":token, "msg": "User logged in correctly"}), 200

@api.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti=get_jwt()["jti"]
    token_blocked=TokenBlockList(jti=jti)
    db.session.add(token_blocked)
    db.session.commit()
    return jsonify({"msg":"Logout"})


@api.route('/userinfo', methods=['GET'])
@jwt_required()
def user_info():
    user=get_jwt_identity()
    payload=get_jwt()
    return jsonify({"user": user, "role": payload["role"]})

@api.route('/private', methods=['GET'])
@jwt_required()
def user_private():
    user=get_jwt_identity()
    return jsonify({"msg": "Access granted", "body": user})
