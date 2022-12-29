import re

from bs4 import BeautifulSoup

from .request import fetch


class Clazz:
    """授業

    識別番号と表示名を持ちます。
    """

    id: str
    displayName: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.displayName = name


class ClazzTable:
    """授業テーブル

    col_count列、row_count行分の授業データを持ちます。
    """

    col_count: int
    row_count: int
    _table: list[list[Clazz | None]]

    def __init__(self, col_count: int, row_count: int) -> None:
        self.col_count = col_count
        self.row_count = row_count
        self._table = [[None for _ in range(row_count)] for _ in range(col_count)]

    def get(self, col: int, row: int) -> Clazz | None:
        return self._table[col][row]

    def set(self, col: int, row: int, clazz: Clazz | None) -> None:
        self._table[col][row] = clazz


def parse_clazz_table(session_token: str) -> ClazzTable | None:
    """授業テーブルを取得します。

    授業テーブルを認証情報を適用して取得します。認証情報が有効かつ取得が成功した場合は該当データ、そのほかの場合はNoneを返します

    Args:
        session_token (str): セッショントークン

    Returns:
        ClazzTable | None: 授業テーブルのデータまたはNone

    Examples:
        >>> import webclass_parser as wp
        >>> clazz_table = wp.parse_clazz_table("6b26a179e3ea1a27bce331e27e6d3385")
    """

    html = fetch(session_token, "index.php")

    if html is None:
        return None

    soup = BeautifulSoup(html, features="html.parser")
    clazz_list_tag = soup.select("table.schedule-table td")

    clazz_table = ClazzTable(6, 8)

    for (i, clazz_tag) in enumerate(clazz_list_tag):
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
