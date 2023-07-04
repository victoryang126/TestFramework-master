import sys
from io import StringIO

# 创建一个StringIO对象
output = StringIO()

# 将sys.stdout重定向到StringIO对象
sys.stdout = output

# 进行print输出
print('Hello, World!')

# 获取保存的输出内容
output_value = output.getvalue()

# 恢复sys.stdout到默认值（屏幕）
sys.stdout = sys.__stdout__

# 关闭StringIO对象
output.close()

# 打印保存的输出内容
# print(output_value)


import sys
from io import StringIO

# 创建一个StringIO对象
output = StringIO()

# 自定义包装函数
# def print_and_save(*args, **kwargs):
#     # 将print的输出重定向到StringIO对象
#     print(*args, **kwargs, file=output)
#     # 将print的输出同时输出到屏幕
#     print(*args, **kwargs)
#
# # 将自定义函数print_and_save替代内置的print函数
# sys.stdout.write = print_and_save

# 调用print函数
print('Hello, World!')

# 获取保存的输出内容
output_value = output.getvalue()

# 关闭StringIO对象
output.close()

# 打印保存的输出内容
print(output_value)

# 改变字体颜色为红色
print('\033[31mHello, World!\033[0m')

# 改变字体颜色为绿色，背景颜色为黄色
print('\033[32;43mHello, World!\033[0m')

# 改变字体颜色为蓝色，加粗文本
print('\033[34;1mHello, World!\033[0m')


print('\033[30;1mHello, World!\033[0m')

def print_black(comment):
    print(f'\033[30;1m{comment}\033[0m')

def print_red(comment):
    print(f'\033[31;1m{comment}\033[0m')

def print_yellow(comment):
    print(f'\033[33;1m{comment}\033[0m')

def print_green(comment):
    print(f'\033[32;1m{comment}\033[0m')

print_red("1")
print_black("2")
print_yellow(3)
print_green(4)
# 30：黑色
# 31：红色
# 32：绿色
# 33：黄色
# 34：蓝色
# 35：洋红色
# 36：青色
# 37：白色
