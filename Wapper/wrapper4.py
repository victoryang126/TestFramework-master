import inspect
import traceback
import logging

def aria_func_decorator(func):
    def wrapper(*args, **kwargs):
        # Get the class name
        class_name = func.__qualname__
        # Get the parameter names and their corresponding values
        signature = inspect.signature(func)
        bound_arguments = signature.bind(*args, **kwargs).arguments
        params = []
        for param_name, param_value in bound_arguments.items():
            params.append(f"{param_name}={param_value}")
        # Concatenate the class name, and parameter information
        message = f"{class_name}, Parameters: {', '.join(params[1:])}"
        try:
            # Call the original function, passing args and kwargs
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            result = func(*args, **kwargs)
            logging.info(f"{timestamp} execute {message}")
            # Check if the function has a return value
            if result is not None:
                return [True, result,timestamp,message]
            else:
                return [True, None,timestamp,message]
        except Exception as e:
            logging.critical(traceback.format_exc())
            return [False, traceback.format_exc(),timestamp,message]

    return wrapper

"""
@classmethod 装饰器位于上方，@decorator 装饰器位于下方。实际应用顺序是先应用 @decorator 装饰器，然后应用 @classmethod 装饰器。因此，装饰器 @decorator 实际上作用于 @classmethod 修饰的方法。
"""
class MyClass:

    @classmethod
    @decorator
    def my_method(cls, x,y, a,b):
        print("Inside my_method")
        # raise  Exception("ttt")
        return 42  # Just an example return value

# Call the decorated method
result = MyClass.my_method(1, 2, a='apple', b='banana')
print(result)
