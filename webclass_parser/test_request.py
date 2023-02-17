from os import environ

from webclass_parser.request import (
    auth_user,
    check_token,
    fetch_clazz_table,
    fetch_notification_list,
)

# セッショントークンの取得
# 使いまわすため読み込み時に実行
try:
    username = environ["WP_USERNAME"]
    password = environ["WP_PASSWORD"]
except KeyError:
    raise Exception("環境変数WP_USERNAMEとWP_PASSWORDにユーザIDとパスワードを設定してください。")
else:
    token = auth_user(username, password)
    if token is None or not check_token(token):
        raise Exception("ユーザ認証に失敗しました。正しいユーザIDとパスワードを設定してください。")


def test_auth_user_failed():
    assert auth_user("wrong_user", "wrong_password") is None


def test_check_token_feiled():
    assert check_token("wrong_token") is False


def test_clazz_table():
    if token is not None:
        clazz_table = fetch_clazz_table(token)
        print(clazz_table)


def test_notification_list():
    if token is not None:
        notification_list = fetch_notification_list(token)
        print(notification_list)
