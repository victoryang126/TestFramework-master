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

def compare_arrays_ignore_order(array1, array2):
    counter1 = Counter(array1)
    counter2 = Counter(array2)
    all_elements = set(array1).union(set(array2))  # 所有出现过的元素
    ret = True
    diff_info = []
    for element in all_elements:
        count1 = counter1.get(element, 0)
        count2 = counter2.get(element, 0)
        if count1 == count2:
            diff_info.append((element, "==",element))
        else:
            diff_info.append((count1 * [element],"!=",count2 * [element]))
            if ret:
                ret = False
    explanation = []
    for diff in diff_info:
        explanation.append(f"Expected: {diff[0]} {diff[1]}  Actual: {diff[2]}")
    return explanation,ret

array1 = [1, 2, 3, 4, 4, 5]
array2 = [5, 2, 3, 4, 4, 5]

diff_info,ret = compare_arrays_ignore_order(array1, array2)
print(diff_info,ret)
#
# for diff in diff_info:
#     print(f"Expected: {diff[0]} {diff[1]}  Actual: {diff[2]}")
