import functools

# 使用 reduce 对列表中的元素进行累积相加
numbers = [1, 2, 3, 4, 5]
sum_result = functools.reduce(lambda x, y: x + y, numbers)
print(sum_result)  # 输出：15

# 使用 reduce 计算阶乘
n = 5
factorial_result = functools.reduce(lambda x, y: x * y, range(1, n+1))
print(factorial_result)  # 输出：120

# 使用 reduce 连接字符串
words = ['Hello', 'World', 'OpenAI', 'GPT']
concatenated_result = functools.reduce(lambda x, y: x + ' ' + y, words)
print(concatenated_result)  # 输出：Hello World OpenAI GPT
