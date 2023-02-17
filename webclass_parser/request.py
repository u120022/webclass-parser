import re

import requests
from bs4 import BeautifulSoup

from webclass_parser.models import Clazz, ClazzTable, Notification, NotificationList


def auth_user(username: str, password: str) -> str | None:
    """ユーザの認証を行います。

    ユーザ名とパスワードでwebclassへの認証を行います。認証が成功した場合はセッショントークン、失敗した場合はNoneを返します。

    Args:
        username (str): ユーザ名
        password (str): パスワード

    Returns:
        str | None: セッショントークンまたはNone

    Examples:
        >>> from webclass_parser.request import auth_user
        >>> session_token = auth_user("VALID_USERNAME", "VALID_PASSWORD")
        >>> print(session_token)
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


def check_token(session_token: str) -> bool:
    """セッショントークンが有効か確認します。

    セッショントークンが現時点で有効か確認します。

    Args:
        session_token (str): セッショントークン

    Returns:
        bool: 有効ならばTrue、無効ならばFalse

    Examples:
        >>> from webclass_parser.request import check_token
        >>> is_valid = check_token("6b26a179e3ea1a27bce331e27e6d3385")
        >>> print(is_valid)
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


def _fetch(session_token: str, rel_path: str) -> str | None:
    """webclass内のサイトのデータを取得します。

    webclass内のサイトのデータを認証情報を適用して取得します。認証情報が有効かつ取得が成功した場合は該当データ、そのほかの場合はNoneを返します

    Args:
        session_token (str): セッショントークン
        rel_path (str): 相対パス

    Returns:
        str | None: 該当サイトのデータまたはNone
    """

    if not check_token(session_token):
        return None

    res = requests.get(
        "https://tpuwcwebsv.pu-toyama.ac.jp/webclass/" + rel_path,
        cookies={"WBT_Session": session_token, "WCAC": "Authenticated"},
    )

    if res.status_code != 200:
        return None

    html = res.text

    return html


def fetch_clazz_table(session_token: str) -> ClazzTable | None:
    """授業テーブルを取得します。

    授業テーブルを認証情報を適用して取得します。認証情報が有効かつ取得が成功した場合は該当データ、そのほかの場合はNoneを返します

    Args:
        session_token (str): セッショントークン

    Returns:
        ClazzTable | None: 授業テーブルのデータまたはNone

    Examples:
        >>> from webclass_parser.request import fetch_clazz_table
        >>> clazz_table = fetch_clazz_table("6b26a179e3ea1a27bce331e27e6d3385")
        >>> print(clazz_table)
    """

    html = _fetch(session_token, "index.php")

    if html is None:
        return None

    soup = BeautifulSoup(html, features="html.parser")
    clazz_list_tag = soup.select("table.schedule-table td")

    clazz_table = ClazzTable(6, 8)

    for i, clazz_tag in enumerate(clazz_list_tag):
        tag = clazz_tag.select_one("a")

        if not tag:
            continue

        ignore_tag = tag.select_one("div")

        if ignore_tag:
            ignore_tag.clear()

        pattern_id = re.search(r"/webclass/course.php/(.*?)/", tag.attrs["href"])
        pattern_displayName = re.search(r"» (.*)", tag.text)

        if not pattern_id or not pattern_displayName:
            continue

        id = pattern_id[1]
        displayName = pattern_displayName[1]
        clazz = Clazz(id, displayName)

        col = i % 7 - 1
        row = i // 7
        clazz_table.set(col, row, clazz)

    return clazz_table


def fetch_notification_list(session_token: str) -> NotificationList | None:
    """お知らせのデータを取得します。

    お知らせのデータを認証情報を適用して取得します。認証情報が有効かつ取得が成功した場合は該当データ、そのほかの場合はNoneを返します

    Args:
        session_token (str): セッショントークン

    Returns:
        NotificationList| None: お知らせのデータまたはNone

    Examples:
        >>> from webclass_parser.request import fetch_notification_list
        >>> notification_list = fetch_notification_list("6b26a179e3ea1a27bce331e27e6d3385")
        >>> print(notification_list)
    """

    html = _fetch(session_token, "informations.php")

    if html is None:
        return None

    soup = BeautifulSoup(html, features="html.parser")

    info_list_tag = soup.select("ul.info-list li.odd,li.eve")
    info_list_tag_count = len(info_list_tag)

    info_list = NotificationList(info_list_tag_count)

    for i, info_tag in enumerate(info_list_tag):
        tag = info_tag.select_one("a")

        if not tag:
            continue

        pattern_id = re.search(r"id=(.*)", tag.attrs["href"])

        if not pattern_id:
            continue

        id = pattern_id[1]
        displayName = tag.text
        info = Notification(id, displayName)

        info_list.set(i, info)

    return info_list
