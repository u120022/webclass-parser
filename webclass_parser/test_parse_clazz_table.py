from webclass_parser.parse_clazz_table import parse_clazz_table


def test_failed_fetch():
    assert parse_clazz_table("_token") is None
