from sqlalchemy import desc

from server import Message


def get_recent_message():
    m = (
        Message.query.order_by(desc(Message.created))
        .filter(Message.message != "")
        .first()
    )
    default_message = " Let's hack! You can submit a PR dynamicdisplay.recurse.com "
    return m.message if m else default_message
