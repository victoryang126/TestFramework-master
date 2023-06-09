import functools

def power(base, exponent):
    return base ** exponent

# 创建一个偏函数，固定 base 参数为 2
power_of_2 = functools.partial(power, base=2)

# 调用偏函数，只需要传递 exponent 参数
result = power_of_2(exponent=3)
print(result)  # 输出：8

# 创建一个偏函数，固定 exponent 参数为 2
square = functools.partial(power, exponent=2)

# 调用偏函数，只需要传递 base 参数
result = square(base=5)
print(result)  # 输出：25

