
import pytest
# 检查两个值是否相等
def test_check_equal():
    assert 2 + 2 == 4

# 检查列表是否包含特定元素
def test_check_list_contains_element():
    my_list = [1, 2, 3, 4, 5]
    assert 3 in my_list

# 检查字符串是否包含特定子字符串
def test_check_string_contains_substring():
    my_string = "Hello, world!"
    assert "world" in my_string

# 检查函数是否引发特定异常
def test_check_exception():
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# 自定义断言消息
def test_custom_message():
    x = 10
    y = 5
    assert x > y, f"{x} 不大于 {y}"

# 使用近似断言
def test_check_float_approximation():
    assert pytest.approx(0.1 + 0.2, 0.0001) == 0.3

#检查集合是否相等：
def test_check_set_equality():
    set1 = {1, 2, 3}
    set2 = {3, 2, 1}
    assert set1 == set2
#检查列表是否按顺序相等：
def test_check_list_order():
    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    assert list1 == list2

#def test_check_dict_key():
    my_dict = {"key1": 1, "key2": 2}
    assert "key1" in my_dict

#检查函数返回值是否符合预期：
def add(x, y):
    return x + y

def test_check_function_result():
    assert add(2, 3) == 5

#检查字符串是否匹配特定模式：
import re

def test_check_string_pattern():
    pattern = r"\d{3}-\d{3}-\d{4}"
    phone_number = "123-456-7890"
    assert re.match(pattern, phone_number)

#def test_check_list_sorted():
    my_list = [5, 2, 8, 1]
    sorted_list = sorted(my_list)
    assert my_list == sorted_list
