def compare_arrays(array1, array2):
    set1 = set(array1)
    set2 = set(array2)
    all_elements = set1.union(set2)  # 所有出现过的元素
    diff_info = []
    for element in all_elements:
        if element in set1 and element in set2:
            diff_info.append((element, element))
        elif element in set1:
            diff_info.append((element, None))
        else:
            diff_info.append((None, element))
    return diff_info

array1 = [1, 2, 3, 4, 5]
array2 = [4, 5, 6, 7, 8]

diff_info = compare_arrays(array1, array2)

for diff in diff_info:
    expected = diff[0]
    actual = diff[1]
    print(f"Expected: {expected}  Actual: {actual}")


