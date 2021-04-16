from sqlalchemy import desc

from app import Message


def get_recent_message():
    m = Message.query.order_by(desc(Message.created)).first()
    default_message = " Let's hack! You can submit a PR dynamicdisplay.recurse.com "
    return m.message if m else default_message
