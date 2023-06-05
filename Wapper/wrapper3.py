import traceback


def decorator(func):
    def wrapper( *args, **kwargs):
        # Get the function name
        function_name = func.__func__.__name__

        # Get the parameter names and their corresponding values
        params = []
        for arg in args:
            params.append(str(arg))
        for key, value in kwargs.items():
            params.append(f"{key}={value}")

        # Concatenate the function name and parameter information
        message = f"Function Name: {function_name}, Parameters: {', '.join(params)}"
        print(message)

        try:
            # Call the original function, passing cls, args, and kwargs
            result = func.__func__( *args, **kwargs)
            print("After function execution")
            # Check if the function has a return value
            if result is not None:
                return [True, result]
            else:
                return [True, None]
        except Exception as e:
            print("Exception occurred")
            return [False, traceback.format_exc()]

    return wrapper


def clsdecorator(func):
    def wrapper( *args, **kwargs):
        # 类方法的限定名称，包括类的名称和方法的名称
        class_func_name = func.__func__.__qualname__
        # print(func.__func__.__module__)
        # Get the function name
        function_name = func.__func__.__name__

        # Get the parameter names and their corresponding values
        params = []
        for arg in args:
            params.append(str(arg))
        for key, value in kwargs.items():
            params.append(f"{key}={value}")

        # Concatenate the class name, function name, and parameter information
        message = f"{class_func_name}, Parameters: {', '.join(params)}"
        print(message)

        try:
            # Call the original function, passing cls, args, and kwargs
            result = func.__func__( *args, **kwargs)
            print("After function execution")
            # Check if the function has a return value
            if result is not None:
                return [True, result]
            else:
                return [True, None]
        except Exception as e:
            print("\n".join(traceback.format_exc().split("\n")[3:]))
            return [False, traceback.format_exc()]

    return wrapper

"""
，实际应用顺序是先应用 @classmethod 装饰器，然后应用 @decorator 装饰器。因此，装饰器 @classmethod 实际上作用于方法，而装饰器 @decorator 则作用于修饰后的方法。
"""
class MyClass:
    @clsdecorator
    @classmethod
    def my_method(cls, *args, **kwargs):
        print("Inside my_method")
        # raise  Exception("ttt")
        return 42  # Just an example return value

# Call the decorated method
result = MyClass.my_method(1, 2, a='apple', b='banana')
print(result)
