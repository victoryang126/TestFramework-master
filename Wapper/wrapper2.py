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

        # Code to execute before calling the original function
        print("Before function execution")

        # Call the original function, passing cls, args, and kwargs
        result = func.__func__( *args, **kwargs)

        # Code to execute after calling the original function
        print("After function execution")

        # Return the result of the original function
        return result

    return wrapper


class MyClass:
    @decorator
    @classmethod
    def my_method(cls, *args, **kwargs):
        print("Inside my_method")

# Call the decorated method
MyClass.my_method(1, 2, a='apple', b='banana')
