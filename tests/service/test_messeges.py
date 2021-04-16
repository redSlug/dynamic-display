from service.messages import get_recent_message


def test_get_message():
    assert get_recent_message()
