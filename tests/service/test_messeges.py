import pytest

from service.messages import get_recent_message


@pytest.mark.skip(reason="skipping for now")
def test_get_message():
    assert get_recent_message()
