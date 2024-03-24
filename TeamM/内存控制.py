
"""
使用生成器和迭代器：生成器和迭代器通常比列表等数据结构更节省内存，因为它们是惰性求值的，只在需要时生成数据。

避免创建不必要的对象：在编程时尽量避免创建不必要的临时对象，特别是对于大型数据集。尽量重用对象或者使用可变对象来避免不必要的拷贝。

使用适当的数据结构：根据需求选择适当的数据结构。例如，如果只需要存储唯一值，可以使用集合而不是列表，因为集合会自动去重。

删除不再需要的对象：及时删除不再需要的对象，特别是在处理大型数据集时。可以使用 del 关键字来删除对象引用，帮助 Python 回收内存。

使用内置函数和模块：Python 内置函数和模块通常会更有效地管理内存，因为它们经过优化并且使用了 C 语言实现。

小心处理文件和网络资源：在处理文件和网络资源时要小心，确保及时关闭文件和释放网络连接，以避免资源泄漏。

避免循环引用：循环引用会导致内存泄漏，因此要小心避免创建循环引用的数据结构。

使用适量的缓存：有时候使用适量的缓存可以提高性能并减少内存消耗，但要注意不要过度依赖缓存，以免引入其他问题。

总的来说，优化内存消耗需要综合考虑代码结构、数据处理方式以及资源管理等方面，根据实际情况进行适当的优化。
"""

# Good example: Using generator function
def generate_numbers(n):
    for i in range(n):
        yield i

# Iterate over generated numbers
for num in generate_numbers(10):
    print(num)

# Bad example: Creating a list instead of using a generator
numbers = [i for i in range(10)]
for num in numbers:
    print(num)

# Good example: Reusing a list
data = [1, 2, 3, 4, 5]
for item in data:
    print(item)

# Bad example: Creating a new list unnecessarily
for item in [1, 2, 3, 4, 5]: #每次循环都会重新创建新对列表
    print(item)

# Good example: Using a set to store unique values
unique_numbers = set([1, 2, 3, 4, 5, 1, 2])
print(unique_numbers)

# Bad example: Using a list instead of a set
unique_numbers = []
for num in [1, 2, 3, 4, 5, 1, 2]:
    if num not in unique_numbers:
        unique_numbers.append(num)
print(unique_numbers)

# Good example: Deleting an object when it's no longer needed
data = [1, 2, 3, 4, 5]
print(data)
del data

# Bad example: Not deleting an object when it's no longer needed
data = [1, 2, 3, 4, 5]
print(data)
# Data still exists in memory but is no longer needed

# Good example: Using built-in function sum()
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(total)

# Bad example: Implementing sum() function manually
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
print(total)


# Good example: Using 'with' statement to handle file
with open('example.txt', 'r') as file:
    data = file.read()
    print(data)
# Bad example: Forgetting to close file
file = open('example.txt', 'r')
data = file.read()
print(data)
# Forgot to close the file


# Good example: Avoiding circular reference
class A:
    pass

class B:
    def __init__(self, a_instance):
        self.a_instance = a_instance

a_instance = A()
b_instance = B(a_instance)
# Bad example: Creating circular reference
class A:
    def __init__(self):
        self.b_instance = B(self)

class B:
    def __init__(self, a_instance):
        self.a_instance = a_instance

a_instance = A()

# Good example: Using caching for expensive computation
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))  # Computes quickly


# Bad example: Recomputing the same values repeatedly
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))  # Slow, recomputes the same values multiple times
