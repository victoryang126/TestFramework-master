def decorator(func):
    def wrapper(*args, **kwargs):
        # 打印函数名称
        print("Function Name:", func.__name__)

        # 打印args和kwargs
        print("Args:", args)
        print("Kwargs:", kwargs)

        # 在调用原始函数之前执行的代码
        print("Before function execution")

        # 调用原始函数，并传递 args 和 kwargs
        result = func(*args, **kwargs)

        # 在调用原始函数之后执行的代码
        print("After function execution")

        # 返回原始函数的结果
        return result

    return wrapper

@decorator
def my_function(*args, **kwargs):
    print("Inside my_function")

# 调用被装饰后的函数
my_function(1, 2, a='apple', b='banana')
