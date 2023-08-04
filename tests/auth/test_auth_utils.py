import pytest

from src.auth.utils import is_email


@pytest.mark.parametrize(
    "credential,expected",
    [
        ("good@mail.com", True),
        ("very.good@mail.ru", True),
        ("1234@mail.com", True),
        ("", False),
        ("myn@me", False),
        ("bad@mail.c", False),
    ]
)
def test_is_email(credential: str, expected: bool) -> None:
    result = is_email(credential)
    assert result == expected
