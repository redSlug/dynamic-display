from sqlalchemy import desc

from server import Message, app
import time
import random

affirming_message = [
    "Habits are fully up to you. Feed the good ones. Starve the toxic ones. Understand you are "
    "never too old to grow new ones. -Dawn Staley",
    "I see beauty in all things",
    "I am so grateful for the discipline and consistency I have with everything I do",
    "Those with a grateful mindset tend to see the message in the mess. And even though life may "
    "knock them down, the grateful find reasons, if even small ones, to get up. -Steve Maraboli",
    "Stop giving your attention to anything that isn't contributing to your happiness. Your "
    "mental health is so much more important.",
    "Believe that you can do it cause you can do it. -Bob Ross",
    "Every time you are tempted to react in the same old way, ask if you want to be a prisoner of the past or a pioneer of the future. --Deepak Chopra",
    "The life of your dreams will happen by design, not by accident. You have to create it in "
    "your mind and then in your space.",
    "The next chapter of your life is going to be so amazing.",
    "To fall in love with yourself is the first secret to happiness",
    "Strength grows in the moments when you think you can't go on but you keep going anyway.",
    "Let things flow naturally to you.",
    "Let go of outcome, focus on journey",
    "Allow adversity to be your teacher.",
    "You'll never be able to control your mood if you let it depend on other people. Decide today that you're the only one in charge of how you feel.",
    "The real difficulty is to overcome how you think about yourself. - Maya Angelou",
    "When a difficult situation comes into our life, it's important to realize that every moment we get to choose the way we want to feel--the way we want to write the narrative of our story. Pick the one that contributes most to your aliveness and growth.",
]


def get_affirming_message():
    random.seed(time.time())
    return random.choice(affirming_message)


def get_recent_user_message():
    with app.app_context():
        m = (
            Message.query.order_by(desc(Message.created))
            .filter(Message.message != "")
            .first()
        )
        default_message = " Let's hack! You can submit a PR dynamicdisplay.recurse.com "
        return m.message if m else default_message
