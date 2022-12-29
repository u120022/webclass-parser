from webclass_parser.parse_info_list import parse_info_list


def test_failed_fetch():
    assert parse_info_list("_token") is None
