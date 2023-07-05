from difflib import SequenceMatcher

def print_diff(left, right):
    matcher = SequenceMatcher(None, left, right)
    opcodes = matcher.get_opcodes()

    # get the difference
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            #
            print(f"{left[i1:i2]} == {right[j1:j2]}")
        elif tag == 'delete':
            # 删除部分
            print(f"{left[i1:i2]} != None")
        elif tag == 'insert':
            # 插入部分
            print(f"None!= {right[j1:j2]}")
        elif tag == 'replace':
            # 替换部分
            print(f"{left[i1:i2]} != {right[j1:j2]}")


def print_diff_with_index(left, right):
    matcher = SequenceMatcher(None, left, right)
    opcodes = matcher.get_opcodes()

    # get the difference
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                print(f"{left[i]} == {right[j]} (left index: {i}, right index: {j})")
        elif tag == 'delete':
            for i in range(i1, i2):
                print(f"{left[i]} != None (left index: {i}, right index: -)")
        elif tag == 'insert':
            for j in range(j1, j2):
                print(f"None != {right[j]} (left index: -, right index: {j})")
        elif tag == 'replace':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                print(f"{left[i]} != {right[j]} (left index: {i}, right index: {j})")


left = [1, 2, 3, 4, 5]
right = [1, 2, 6, 4, 5,7]

print_diff(left, right)
print_diff("AB", "CD")
print_diff( bytearray([0x01,0x02]),  bytearray([0x02,0x02]))

print_diff_with_index(left, right)
print_diff_with_index("AB", "CD")
print_diff_with_index( bytearray([0x01,0x02]),  bytearray([0x02,0x02]))
