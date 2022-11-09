from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import random
import datetime
# from flask_jwt_extended import create_access_token, get_jwt_identity
from uuid import uuid4

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/traveloggers"


mongo = PyMongo(app)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return('HEllo MF')


@app.route("/login")
def login():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    user = mongo.db.users.find_one({"email": email})
    user_id = user["_id"]

    if user:
        print("user found")
        if bcrypt.check_password_hash(user.get("password"), password):
            # access_token = create_access_token(
            #     identity=email, additional_claims={"is_administrator": True}
            # )

            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Login successful",
                        "id": user_id,
                    }
                )
            )

    return {
        "success": False,
        "message": "incorrect username or password",
        "data": [],
    }


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        First_name = request.get_json().get("First_name")
        Last_name = request.get_json().get("Last_name")
        City = request.get_json().get("City")
        State = request.get_json().get("State")
        Email = request.get_json().get("Email")
        Password = request.get_json().get("Password")

        hashpw = bcrypt.generate_password_hash(Password).decode("utf-8")

        mongo.db.users.insert_one(
            {
                "_id": str(uuid4()),
                "fname": First_name,
                "lname": Last_name,
                "city": City,
                "state": State,
                "email": Email,
                "password": hashpw

            }
        )

        return(
            jsonify({
                "success": True,
                "message": "User created!"
            })
        )
    return({
        "success": False,
        "message": "You cant create account FO"
    })


# @auth_api.post("/login")
# def login():
#     username = request.get_json().get("username")
#     password = request.get_json().get("password")
#     user = mongo.db.users.find_one({"username": username})

#     if user:
#         print("user found")
#         if bcrypt.check_password_hash(user.get("password"), password):
#             access_token = create_access_token(
#                 identity=username, additional_claims={"is_administrator": True}
#             )
#             return (
#                 jsonify(
#                     {
#                         "success": True,
#                         "message": "Login successful",
#                         "data": {"access_token": access_token},
#                     }
#                 ),
#                 200,
#             )

#         return {
#             "success": False,
#             "message": "incorrect username and password",
#             "data": [],
#         }, 200


if __name__ == "__main__":
    app.secret_key = "asdtc"
    app.run(debug=True)
