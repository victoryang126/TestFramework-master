from collections import Counter

def compare_arrays(array1, array2):
    counter1 = Counter(array1)
    counter2 = Counter(array2)
    all_elements = set(array1).union(set(array2))  # 所有出现过的元素
    diff_info = []
    for element in all_elements:
        count1 = counter1.get(element, 0)
        count2 = counter2.get(element, 0)
        if count1 != count2:
            diff_info.append((element, count1, count2))

    if not diff_info:
        print("Arrays are identical")
        return True
    else:
        print("Arrays have differences:")
        for diff in diff_info:
            element = diff[0]
            count1 = diff[1]
            count2 = diff[2]
            print(f"Element: {element} | Count in Array1: {count1} | Count in Array2: {count2}")
        return False

array1 = [1, 2, 3, 4, 4, 5]
array2 = [4, 5, 5, 6, 7, 8]

result = compare_arrays(array1, array2)
print("Arrays are identical:", result)


from collections import Counter

def compare_arrays(array1, array2):
    counter1 = Counter(array1)
    counter2 = Counter(array2)
    all_elements = set(array1).union(set(array2))  # 所有出现过的元素
    diff_info = []
    for element in all_elements:
        count1 = counter1.get(element, 0)
        count2 = counter2.get(element, 0)
        if count1 == count2:
            diff_info.append((element, "=="))
        else:
            diff_info.append((count1 * [element], count2 * [element]))
    return diff_info

array1 = [1, 2, 3, 4, 4, 5]
array2 = [4, 5, 5, 6, 7, 8]

diff_info = compare_arrays(array1, array2)

for diff in diff_info:
    expected = diff[0]
    actual = diff[1]
    print(f"Expected: {expected}  Actual: {actual}")
