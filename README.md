# webclass-parser

![workflow](https://github.com/u120022/webclass-parser/actions/workflows/lint.yml/badge.svg)
![workflow](https://github.com/u120022/webclass-parser/actions/workflows/test.yml/badge.svg)

## Usage

```python
from webclass-parser.request import auth_user, check_token, fetch_clazz_table

token = wp.auth_user(username="XXX", password="XXX")

if token is None or not check_token(token):
  raise Exception("failed to auth user")

clazz_table = fetch_clazz_table(token)
print(clazz_table)
```
