import inspect
import logging
import traceback
import datetime

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

            logging.info(f"{timestamp} execute {message}")

            # Check if the function has a return value
            if result is not None:
                return [True, result, timestamp, message]
            else:
                return [True, None, timestamp, message]
        except Exception as e:
            logging.critical(traceback.format_exc())
            return [False, traceback.format_exc(), timestamp, message]

    @classmethod
    def my_additional_decorator(cls, func):
        def wrapper(*args, **kwargs):
            # Perform additional decoration logic...
            # For example, you can modify the arguments or manipulate the result
            class_name = func.__qualname__

            # Get the parameter names and their corresponding values
            signature = inspect.signature(func)
            bound_arguments = signature.bind(*args, **kwargs).arguments
            params = []
            for param_name, param_value in bound_arguments.items():
                params.append(f"{param_name}={param_value}")

            # Concatenate the class name and parameter information
            message = f"{class_name}, Parameters: {', '.join(params[1:])}"

            try:
                # Call the original function, passing args and kwargs
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                result = func(*args, **kwargs)

                logging.info(f"{timestamp} execute {message}")

                # Check if the function has a return value
                if result is not None:
                    return [True, result, timestamp, message]
                else:
                    return [True, None, timestamp, message]
            except Exception as e:
                logging.critical(traceback.format_exc())
                return [False, traceback.format_exc(), timestamp, message]

        return wrapper


# Example usage
# @AriaFuncDecorator
@AriaFuncDecorator.my_additional_decorator
def my_function(param1, param2):
    # Function logic...
    return "Hello, World!"

result = my_function("param1_value", "param2_value")
print(result)
