import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
import psycopg2

load_dotenv()

app = Flask(__name__)

conn = psycopg2.connect(dbname="discounthub", user=os.environ.get("DBUSER"), password=os.environ.get("DBPASS"), host=os.environ.get("DBHOST"), port=os.environ.get("DBPORT"))

# [POST] /register?email=<email>
@app.route("/register", methods=["POST"])
def register_user():
    email = request.args.get("email")
    if email is None:
        return "Bad request", 400

    print("Register user {}".format(email))

    # TODO add user to db
    return "Ok", 200

# [GET] /nearby?loc=<location>&r=<radius>
@app.route("/nearby", methods=["GET"])
def find_nearby():
    location = request.args.get("loc")
    radius = request.args.get("r")
    if location is None or radius is None:
        return "Bad request", 400

    print("Get discounts {} away from {}".format(radius, location))

    # TODO get discounts within radius from db
    return "Ok", 200

# [GET] /discount?id=<id>
@app.route("/discount", methods=["GET"])
def get_discount():
    id = request.args.get("id")
    if id is None:
        return "Bad request", 400
    print("Get discount with id {}".format(id))

    # TODO get discount from db
    return "Ok", 200

# [POST] /discount?user=<email>&loc=<location>&t=<title>&desc=[description]&req=<requirement>&amnt=<amount>
@app.route("/discount", methods=["POST"])
def post_discount():
    email = request.args.get("user")
    location = request.args.get("loc")
    title = request.args.get("t")
    description = request.args.get("desc")
    requirement = request.args.get("req")
    amount = request.args.get("amnt")
    if email is None or location is None or requirement is None or amount is None or title is None:
        return "Bad request", 400

    print("User {} uploads discount at {}({}): {} off if you are {}. {}".format(email, title, location, amount, requirement, description))

    # TODO add discount to db
    # TODO add positive update to discount
    return "Ok", 200

# [POST] /rate?user=<email>&did=<discount_id>&fb=<feedback>
@app.route("/rate", methods=["post"])
def post_feedback():
    email = request.args.get("user")
    discount_id = request.args.get("did")
    feedback = request.args.get("fb")
    if email is None or discount_id is None or feedback is None:
        return "Bad request", 400

    print("User {} rates discount with id {} as {}".format(email, discount_id, feedback))

    # TODO add feedback to db
    return "Ok", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))