import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
import psycopg2

load_dotenv()

app = Flask(__name__)

conn = psycopg2.connect(db="discounthub", user = os.environ.get("DBUSER"), password=os.environ.get("DBPASS"), host=os.environ.get("DBHOST"), port=os.environ.get("DBPORT"))

# [POST] /register?email=<email>
@app.route("/register", methods=["POST"])
def register_user():
    email = request.args.get("email")

    # TODO add user to db

# [GET] /nearby?loc=<location>&r=<radius>
@app.route("/nearby", methods=["GET"])
def find_nearby():
    location = request.args.get("loc")
    radius = request.args.get("r")

    # TODO get discounts within radius from db

# [GET] /discount?id=<id>
@app.route("/discount", methods=["GET"])
def get_discount():
    id = request.args.get("id")

    # TODO get discount from db

# [POST] /discount?user=<email>&loc=<location>&req=<requirement>&amnt=<amount>
@app.route("/discount", methods=["POST"])
def post_discount():
    email = request.args.get("user")
    location = request.args.get("loc")
    requirement = request.args.get("req")
    amount = request.args.get("amnt")

    # TODO add discount to db
    # TODO add positive update to discount

# [POST] /rate?user=<email>&fb=<feedback>
@app.route("/rate", methods=["post"])
def post_feedback():
    email = request.args.get("user")
    feedback = request.args.get("fb")

    # TODO add feedback to db


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))