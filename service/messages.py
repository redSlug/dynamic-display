from sqlalchemy import desc

from server import Message
import random

affirming_message = [
    "I see beauty in all things",
    "I am so grateful for the discipline and consistency I have with everything I do",
    "Those with a grateful mindset tend to see the message in the mess. And even though life may "
    "knock them down, the grateful find reasons, if even small ones, to get up. -Steve Maraboli",
]


def get_recent_message(display_affirming_message):
    if display_affirming_message:
        return random.choice(affirming_message)

    m = (
        Message.query.order_by(desc(Message.created))
        .filter(Message.message != "")
        .first()
    )
    default_message = " Let's hack! You can submit a PR dynamicdisplay.recurse.com "
    return m.message if m else default_message
