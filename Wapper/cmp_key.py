import functools

def compare_length(a, b):
    if len(a) < len(b):
        return -1
    elif len(a) > len(b):
        return 1
    else:
        return 0

names = ['Alice', 'Bob', 'Charlie', 'Dave']
sorted_names = sorted(names, key=functools.cmp_to_key(compare_length))
print(sorted_names)  # 输出：['Bob', 'Dave', 'Alice', 'Charlie']
