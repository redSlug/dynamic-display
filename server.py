import os

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, String, Integer
from sqlalchemy.sql import func

from service.util import DB_URL


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    author = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "hello"


@app.route("/matrix/api/message", methods=["POST"])
def create_message():
    try:
        data = request.get_json()
        if "message" not in data:
            return jsonify({"error": "bad payload"}), 400
        message = data.get("message")
        author = data.get("author")

        msg = Message(message=message, author=author)

        db.session.add(msg)
        db.session.commit()
        db.session.flush()
        return (
            jsonify(dict(message=message, author=author)),
            200,
        )
    except Exception as e:
        return jsonify(dict(exception=e)), 400


@app.route("/matrix/api/message", methods=["GET"])
def get_messages():
    try:
        messages = Message.query.all()
        messages = [
            dict(
                id=str(m.id),
                created=m.created.strftime("%Y-%m-%d %H:%M:%S"),
                author=m.author,
                message=str(m.message),
            )
            for m in messages
        ]
        return jsonify(dict(messages=messages)), 200
    except Exception as e:
        return jsonify(dict(exception=e)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0")
