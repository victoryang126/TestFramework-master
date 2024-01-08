

def are_bytearrays_all_different(array_2d):
    seen_bytearrays = set()
    for row in array_2d:
        for byte_array in row:
            if bytes(byte_array) in seen_bytearrays:
                return False
            seen_bytearrays.add(bytes(byte_array))
    return True

def are_bytearrays_all_same(array_2d):
    if not array_2d or not array_2d[0]:
        return False
    first_bytearray = array_2d[0][0]
    for row in array_2d:
        for byte_array in row:
            if byte_array != first_bytearray:
                return False
    return True


def has_duplicate(matrix):
    seen_values = set()
    for row in matrix:
        for value in row:
            if value in seen_values:
                return True
            seen_values.add(value)
    return False

def is_bytearray_all_zeros(byte_array, expected_length):
    if len(byte_array) != expected_length:
        return False
    return all(value == 0 for value in byte_array)


def is_bytearray_in_2d_array(target_bytearray, array_2d):
    for row in array_2d:
        if target_bytearray in row:
            return True
    return False

if __name__ == "__main__":
    # 示例用法
    # my_bytearray = bytearray(b'\x00\x00\x00\x00')
    # expected_length = 4
    # if is_bytearray_all_zeros(my_bytearray, expected_length):
    #     print("所有值都是零且数组长度符合预期")
    # else:
    #     print("存在非零值或数组长度不符合预期")
    # # 示例用法
    # my_matrix = [
    #     bytearray(b'\x01\x02\x03'),
    #     bytearray(b'\x04\x05\x06'),
    #     bytearray(b'\x07\x08\x09')
    # ]
    #
    # if has_duplicate(my_matrix):
    #     print("存在重复值")
    # else:
    #     print("没有重复值")

    # 示例用法
    my_2d_array = [
        bytearray(b'\x01\x02\x03'),
        bytearray(b'\x04\x05\x06'),
        bytearray(b'\x07\x08\x09')
    ]

    target_bytearray = bytearray(b'\x04\x07\x06')

    if is_bytearray_in_2d_array(target_bytearray, my_2d_array):
        print("bytearray在二维数组中")
    else:
        print("bytearray不在二维数组中")


        # 示例用法
    my_2d_array_different = [
        bytearray(b'\x01\x02\x03'),
        bytearray(b'\x04\x05\x06'),
        bytearray(b'\x07\x08\x09')
    ]

    my_2d_array_same = [
        bytearray(b'\x01\x01\x01'),
        bytearray(b'\x01\x01\x01'),
        bytearray(b'\x01\x01\x01')
    ]

    if are_bytearrays_all_different(my_2d_array_different):
        print("二维数组中的bytearrays全部不同")
    else:
        print("二维数组中的bytearrays不全部不同")

    if are_bytearrays_all_same(my_2d_array_same):
        print("二维数组中的bytearrays全部相同")
    else:
        print("二维数组中的bytearrays不全部相同")
