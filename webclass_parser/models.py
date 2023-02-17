class Clazz:
    """授業

    識別番号と表示名を持ちます。
    """

    id: str
    displayName: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.displayName = name

    def __str__(self) -> str:
        return self.displayName


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

    def __str__(self) -> str:
        text = ""
        for col in range(self.col_count):
            text += col.__str__()
            for row in range(self.row_count):
                text += ", "
                text += self.get(col, row).__str__()
            text += "\n"
        return text


class Notification:
    """お知らせの項目

    識別番号と表示名を持ちます。
    """

    id: str
    displayName: str

    def __init__(self, id: str, displayName: str) -> None:
        self.id = id
        self.displayName = displayName

    def __str__(self) -> str:
        return self.displayName


class NotificationList:
    """お知らせ

    count個分のお知らせの項目のデータを持ちます。
    """

    count: int
    _list: list[Notification | None]

    def __init__(self, count: int) -> None:
        self.count = count
        self._list = [None for _ in range(count)]

    def get(self, index: int) -> Notification | None:
        return self._list[index]

    def set(self, index: int, info: Notification | None) -> None:
        self._list[index] = info

    def __str__(self) -> str:
        text = ""
        for i in range(self.count):
            text += self.get(i).__str__()
            text += "\n"
        return text
