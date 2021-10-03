import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, String, Integer
from sqlalchemy.sql import func

load_dotenv(find_dotenv(filename="dotenv"))

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
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


@app.route("/<string:page_name>/")
def static_page(page_name):
    return render_template("%s.html" % page_name)


@app.route("/matrix/api/message", methods=["POST"])
def create_message():
    data = request.get_json()
    if "message" not in data:
        return jsonify({"error": "bad payload"}), 400
    message = data.get("message")
    author = data.get("author")

    msg = Message(message=message, author=author)

    db.session.add(msg)
    db.session.commit()
    db.session.close()
    return (
        jsonify(dict(data=msg.id, created=msg.created, id=msg.id, author=msg.author)),
        200,
    )


@app.route("/matrix/api/message", methods=["GET"])
def get_messages():
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")