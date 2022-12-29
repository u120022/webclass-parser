from webclass_parser.request import auth, check, fetch


def test_failed_auth():
    assert auth("_username", "_password") is None


def test_failed_check():
    assert check("_token") is False


def test_failed_fetch():
    assert fetch("_token", "") is None


def test_failed_fetch_not_found():
    assert fetch("_token", "_not_found") is None
