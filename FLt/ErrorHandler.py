def divide_numbers(a, b):
    try:
        result = a / b
        print("结果：", result)
    except ZeroDivisionError:
        print("除数不能为零！")
    except TypeError:
        print("输入的数据类型不正确！")
    except Exception as e:
        print("发生了一个未知错误：", str(e))

# 测试错误处理程序
divide_numbers(10, 2)   # 正常情况，输出结果：5.0

divide_numbers(10, 0)   # 除以零，捕获 ZeroDivisionError，输出结果：除数不能为零！

divide_numbers(10, '2')  # 类型错误，捕获 TypeError，输出结果：输入的数据类型不正确！

divide_numbers(10, [])   # 发生未知错误，捕获 Exception，输出结果：发生了一个未知错误： unsupported operand type(s) for /: 'int' and 'list'
