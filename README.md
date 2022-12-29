# webclass-parser

![workflow](https://github.com/u120022/webclass-parser/actions/workflows/lint.yml/badge.svg)
![workflow](https://github.com/u120022/webclass-parser/actions/workflows/test.yml/badge.svg)

## Usage

```python
import webclass_parser as wp

token = wp.auth(username="XXX", password="XXX")

if token is None:
  raise Exception("failed to fetch valid token")

if not wp.check(token):
  raise Exception("invalid token")

clazz_table = wp.parse_clazz_table(token)

if clazz_table is None:
  raise Exception("failed to fetch valid class table")

for col in range(clazz_table.col_count):
  for row in range(clazz_table.row_count):
    clazz = clazz_table.get(col=col, row=row)

    if clazz:
      print(clazz.displayName, end=", ")
    else:
      print("empty", end=", ")
  print()
```
