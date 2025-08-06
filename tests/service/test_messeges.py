import pytest

from service.messages import get_affirming_message, get_recent_user_message, affirming_message


@pytest.mark.skip(reason="skipping for now")
def test_get_message():
    assert get_recent_user_message(False)


def test_get_affirming_message():
    assert get_affirming_message() in affirming_message
