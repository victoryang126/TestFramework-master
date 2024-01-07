import traceback
import can

def step():
    try:
        assert [1,2]==[1,1]
    except AssertionError as e:
        print("Assertion failed:", str(e))
        traceback.print_exc()
        # print(traceback.format_exc())

# from assertpy import assert_that
#
# value = 42
#
# # 使用 assertpy 进行断言
# assert_that([1,2]).is_equal_to([1,1])
# assert_that(value).is_instance_of(int)
# assert_that(value).is_greater_than(0)

# from hamcrest import assert_that, equal_to, has_length, contains_string
#
# value = "Hello, World!"
# numbers = [1, 2, 3, 4, 5]
#
# # 使用 PyHamcrest 进行断言
# assert_that(value, equal_to("Hello, Worrld!"))  # 断言相等性
# assert_that(value, contains_string("World"))  # 断言包含子字符串
# assert_that(numbers, has_length(5))  # 断言列表长度为 5

from nose.tools import assert_equal, assert_in

value = "Hello, World!"
numbers = [1, 2, 3, 4, 5]

# 使用 nose 进行断言
try:
    assert_equal(value, "Hello, Worle!")  # 断言相等性
except Exception as e:
    print(e)
    print(traceback.format_exc())
# assert_in("World", value)  # 断言字符串包含
# assert_equal(len(numbers), 5)  # 断言列表长度为 5
