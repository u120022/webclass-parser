import re

from bs4 import BeautifulSoup

from .request import fetch


class Info:
    """お知らせの項目

    識別番号と表示名を持ちます。
    """

    id: str
    displayName: str

    def __init__(self, id: str, displayName: str) -> None:
        self.id = id
        self.displayName = displayName


class InfoList:
    """お知らせ

    count個分のお知らせの項目のデータを持ちます。
    """

    count: int
    _list: list[Info | None]

    def __init__(self, count: int) -> None:
        self.count = count
        self._list = [None for _ in range(count)]

    def get(self, index: int) -> Info | None:
        return self._list[index]

    def set(self, index: int, info: Info | None) -> None:
        self._list[index] = info


def parse_info_list(session_token: str) -> InfoList | None:
    """お知らせのデータを取得します。

    お知らせのデータを認証情報を適用して取得します。認証情報が有効かつ取得が成功した場合は該当データ、そのほかの場合はNoneを返します

    Args:
        session_token (str): セッショントークン

    Returns:
        InfoList | None: お知らせのデータまたはNone

    Examples:
        >>> import webclass_parser as wp
        >>> info_list = wp.parse_info_list("6b26a179e3ea1a27bce331e27e6d3385")
    """

    html = fetch(session_token, "informations.php")

    if html is None:
        return None

    soup = BeautifulSoup(html, features="html.parser")

    info_list_tag = soup.select("ul.info-list li.odd,li.eve")
    info_list_tag_count = len(info_list_tag)

    info_list = InfoList(info_list_tag_count)

    for (i, info_tag) in enumerate(info_list_tag):
        tag = info_tag.select_one("a")

        if not tag:
            continue

        pattern_id = re.search(r"id=(.*)", tag.attrs["href"])

        if not pattern_id:
            continue

        id = pattern_id[1]
        displayName = tag.text
        info = Info(id, displayName)

        info_list.set(i, info)

    return info_list
