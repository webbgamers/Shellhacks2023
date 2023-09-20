import os
import datetime
from dotenv import load_dotenv

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import psycopg2

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://find.nearus.xyz","https://find.nearus.xyz"])

conn = psycopg2.connect(dbname="discounthub", user=os.environ.get("DBUSER"), password=os.environ.get("DBPASS"), host=os.environ.get("DBHOST"), port=os.environ.get("DBPORT"))

# Redirect root to GitHub
@app.route("/")
def redirect_root():
    return redirect("https://github.com/webbgamers/discount-hub-api/")


# [POST] /register?email=<email>
@app.route("/register", methods=["POST"])
def register_user():
    email = request.args.get("email")
    if email is None:
        return jsonify({"error":"Missing argument"}), 400

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO public.users (email)
            VALUES (%s) RETURNING id
            """,
            (email,)
        )
    except:
        cur.execute("ROLLBACK")
        conn.commit()
        cur.close()
        return jsonify({"error":"Internal error"}), 500

    id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({"id":id}), 201

# [GET] /nearby?loc=<location>&r=<radius>
@app.route("/nearby", methods=["GET"])
def find_nearby():
    location = request.args.get("loc")
    radius = request.args.get("r")
    if location is None or radius is None:
        return jsonify({"error":"Missing argument"}), 400

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, ST_AsText(ST_FlipCoordinates(location)), requirement, amount, title, description FROM public.discounts
            WHERE ST_Distance(ST_Transform(ST_SetSRID(ST_FlipCoordinates(ST_GeometryFromText(%s)), 4326), 3857), ST_Transform(public.discounts.location, 3857)) < %s;
            """,
            ("POINT({})".format(location), radius)
        )
    except:
        cur.execute("ROLLBACK")
        conn.commit()
        cur.close()
        return jsonify({"error":"Internal error"}), 500

    results = []
    for r in cur:
        results.append({"id":r[0], "location":r[1][6:-1], "requirement":r[2], "amount":r[3], "title":r[4], "description":r[5]})

    conn.commit()
    cur.close()
    return jsonify(results), 200

# [GET] /discount?id=<id>
@app.route("/discount", methods=["GET"])
def get_discount():
    id = request.args.get("id")
    if id is None:
        return jsonify({"error":"Missing argument"}), 400

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, ST_AsText(ST_FlipCoordinates(location)), requirement, amount, title, description FROM public.discounts
            WHERE public.discounts.id = %s
            """,
            (id,)
        )
    except:
        cur.execute("ROLLBACK")
        conn.commit()
        cur.close()
        return jsonify({"error":"Internal error"}), 500
    
    d = cur.fetchone()

    cur.close()

    if d is None:
        return jsonify({"error":"Not found"}), 404
    return jsonify({"id":d[0], "location":d[1][6:-1], "requirement":d[2], "amount":d[3], "title":d[4], "description":d[5]}), 200

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
        return jsonify({"error":"Missing argument"}), 400

    cur = conn.cursor()

    try:
        cur.execute("""
            with rows as (
                INSERT INTO public.discounts (location, requirement, amount, title, description)
                VALUES (ST_SetSRID(ST_FlipCoordinates(ST_GeomFromText(%s)), 4326), %s, %s, %s, %s)
                RETURNING id
            )

            INSERT INTO public.updates (discount_id, user_id, post_date, feedback)
            VALUES ((SELECT id FROM rows),(
                SELECT id FROM public.users
                WHERE public.users.email = %s
            ),%s,'good')
            RETURNING discount_id
            """,
            ("POINT({})".format(location), requirement, amount, title, description, email, datetime.datetime.now())
        )
    except:
        cur.execute("ROLLBACK")
        conn.commit()
        cur.close()
        return jsonify({"error":"Internal error"}), 500

    id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    return jsonify({"id":id}), 201

# [POST] /rate?user=<email>&did=<discount_id>&fb=<feedback>
@app.route("/rate", methods=["POST"])
def post_feedback():
    email = request.args.get("user")
    discount_id = request.args.get("did")
    feedback = request.args.get("fb")
    if email is None or discount_id is None or feedback is None:
        return jsonify({"error":"Missing argument"}), 400

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO public.updates (discount_id, user_id, post_date, feedback)
            VALUES (%s,(
                SELECT id FROM public.users
                WHERE public.users.email = %s
            ),%s,%s)
            RETURNING id
            """,
            (discount_id, email, datetime.datetime.now(), feedback)
        )
    except:
        cur.execute("ROLLBACK")
        conn.commit()
        cur.close()
        return jsonify({"error":"Internal error"}), 500
        

    id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    return jsonify({"id":id}), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
