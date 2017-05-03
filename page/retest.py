import re

print(re.search("^[0-9'.']", "5.1分"))
print(re.match("[0-9]", "¥11195/人起"))
