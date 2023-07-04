def compare_elements(element1, element2):
    len1 = len(element1)
    len2 = len(element2)
    if len1 != len2:
        print(f"Arrays have different lengths: {len1} != {len2}")
        return False

    differences = []
    for i, (e1, e2) in enumerate(zip(element1, element2)):
        if e1 != e2:
            differences.append((i, e1, e2))

    if differences:
        for i, e1, e2 in differences:
            print(f"Elements at position {i} are not equal: {e1} != {e2}")
        return False

    return True



list1 = [1, 2, 3]
list2 = [1, 4, 4,5]
result = compare_elements(list1, list2)

compare_elements("AB", "CD")


