from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST
from sqlalchemy import or_
from flask import current_app
import requests
import os
# from task import send_user_registration_email
from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema


# blueprint is used to divide the api into multiple segments, here we have item, store and tags
blp = Blueprint("Users", "users", description="Operations on users")


def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    key = os.getenv("MAILGUN_API_KEY")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", key),
        data={
            "from": f"Vinay Kumar <mailgun@{domain}>",
            "to": to,
            "subject": subject,
            "text": body,
        }
    )


# here we are registering the user
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        # checking if the user is already registered
        if UserModel.query.filter(
            or_(UserModel.username == user_data["username"],
                UserModel.email == user_data["email"])).first():
            abort(409, message="A user with this username or email already exists")
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(
                user_data["password"])  # hashing the password
        )

        db.session.add(user)
        db.session.commit()
        send_simple_message(
            to=user.email,
            subject="Successfully signed up",
            body=f"Hi {user.username}! You have successfully signed up to the Stores REST API."
        )
        return {"message": "User registered successfully"}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, "Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}


# we are making refresh so that the user don't have to make the access token again and again
# it will make login once and then we will generate two tokens- an access token and a refresh token
# the refresh token will then keep generating the new access token, when the time expires, but those new access tokens
# will be non-fresh, so they could be used to get the information or related work
# but for destructive access like delete, it will have to login again and get the access token
@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
