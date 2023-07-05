from difflib import SequenceMatcher

# 创建 SequenceMatcher 对象
s1 = "abcdef"
s2 = "abcd1234ef"
matcher = SequenceMatcher(None, s1, s2)

# 获取操作列表
opcodes = matcher.get_opcodes()

# 打印操作列表
print("Operation Codes:")
for tag, i1, i2, j1, j2 in opcodes:
    print(f"Tag: {tag}, Indices: ({i1}, {i2}), ({j1}, {j2})")
