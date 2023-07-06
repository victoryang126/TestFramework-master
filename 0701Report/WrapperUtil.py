import inspect
import traceback
import logging
import datetime
from typing import TypeVar,Generic,List,Union
import time

# T = TypeVar("T")
# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s -%(levelname)s - %(message)s')

class AriaFuncDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # Get the class name
        class_name = self.func.__qualname__

        # Get the parameter names and their corresponding values
        signature = inspect.signature(self.func)
        bound_arguments = signature.bind(*args, **kwargs).arguments
        params = []
        for param_name, param_value in bound_arguments.items():
            params.append(f"{param_name}={param_value}")

        # Concatenate the class name and parameter information
        message = f"{class_name}, Parameters: {', '.join(params[1:])}"

        try:
            # Call the original function, passing args and kwargs
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            result = self.func(*args, **kwargs)

            # logging.info(f"{timestamp} execute {message}")

            # Check if the function has a return value
            if result is not None:
                return [True, result, timestamp, message]
            else:
                return [True, None, timestamp, message]
        except Exception as e:
            # logging.critical(traceback.format_exc())
            return [False, str(e), timestamp, message]

    @classmethod
    def func_excute_duration(cls, func):
        def wrapper(*args, **kwargs):
            # Perform additional decoration logic...
            # For example, you can modify the arguments or manipulate the result
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            logging.info(f"Execution Time: {execution_time:.6f} seconds")

            return result

        return wrapper


#
# def aria_func_decorator(func):
#     def wrapper(*args, **kwargs):
#         # Get the class name
#         class_name = func.__qualname__
#         # Get the parameter names and their corresponding values
#         signature = inspect.signature(func)
#         bound_arguments = signature.bind(*args, **kwargs).arguments
#         params = []
#         for param_name, param_value in bound_arguments.items():
#             params.append(f"{param_name}={param_value}")
#         # Concatenate the class name, and parameter information
#         message = f"{class_name}, Parameters: {', '.join(params[1:])}"
#         try:
#             # Call the original function, passing args and kwargs
#             timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#             result = func(*args, **kwargs)
#             # logging.info(f"{timestamp} execute {message}")
#             # Check if the function has a return value
#             if result is not None:
#                 return [Result.passed, result,timestamp,message]
#             else:
#                 return [Result.passed, None,timestamp,message]
#         except Exception as e:
#             logging.critical(traceback.format_exc())
#             return [Result.failed, str(e),timestamp,message]
#
#     return wrapper