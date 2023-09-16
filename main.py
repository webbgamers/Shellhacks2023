import os
from dotenv import load_dotenv

from flask import Flask
import psycopg2

load_dotenv()

app = Flask(__name__)

conn = psycopg2.connect(database=os.environ.get("DB"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"), host = os.environ.get("DBHOST"), port = os.environ.get("DBPORT"))


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))