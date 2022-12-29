import requests


def auth(username: str, password: str) -> str | None:
    """ユーザの認証を行います。

    ユーザ名とパスワードでwebclassへの認証を行います。認証が成功した場合はセッショントークン、失敗した場合はNoneを返します。

    Args:
        username (str): ユーザ名
        password (str): パスワード

    Returns:
        str | None: セッショントークンまたはNone

    Examples:
        >>> import webclass_parser as wp
        >>> session_token = wp.auth("VALID_USERNAME", "VALID_PASSWORD")
    """

    res = requests.post(
        "https://tpuwcwebsv.pu-toyama.ac.jp/webclass/login.php",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "val": password},
    )

    if res.status_code != 200:
        return None

    if "WCAC" not in res.cookies or "WBT_Session" not in res.cookies:
        return None

    status = res.cookies["WCAC"]
    session_token = res.cookies["WBT_Session"]

    if status != "Authenticated":
        return None

    return session_token


def check(session_token: str) -> bool:
    """セッショントークンが有効か確認します。

    セッショントークンが現時点で有効か確認します。

    Args:
        session_token (str): セッショントークン

    Returns:
        bool: 有効ならばTrue、無効ならばFalse

    Examples:
        >>> import webclass_parser as wp
        >>> is_valid = wp.check("6b26a179e3ea1a27bce331e27e6d3385")
    """

    res = requests.get(
        "https://tpuwcwebsv.pu-toyama.ac.jp/webclass/login.php",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        cookies={"WBT_Session": session_token},
    )

    if res.status_code != 200:
        return False

    if "WCAC" not in res.cookies:
        return False

    status = res.cookies["WCAC"]

    if status != "Authenticated":
        return False

    return True


def fetch(session_token: str, rel_path: str) -> str | None:
    """webclass内のサイトのデータを取得します。

    webclass内のサイトのデータを認証情報を適用して取得します。認証情報が有効かつ取得が成功した場合は該当データ、そのほかの場合はNoneを返します

    Args:
        session_token (str): セッショントークン
        rel_path (str): 相対パス

    Returns:
        str | None: 該当サイトのデータまたはNone

    Examples:
        >>> import webclass_parser as wp
        >>> res = wp.fetch("6b26a179e3ea1a27bce331e27e6d8285")
    """

    if not check(session_token):
        return None

    res = requests.get(
        "https://tpuwcwebsv.pu-toyama.ac.jp/webclass/" + rel_path,
        cookies={"WBT_Session": session_token, "WCAC": "Authenticated"},
    )

    if res.status_code != 200:
        return None

    html = res.text

    return html
