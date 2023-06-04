# class CustomAssertionError(AssertionError):
#     def __init__(self, message, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.message = message
#
# def custom_assert(condition, message):
#     if not condition:
#         raise CustomAssertionError(message)
#
# def divide(a, b):
#     custom_assert(b != 0, "除数不能为零")
#     return a / b

# try:
#     custom_assert(b != 0, "除数不能为零")
# except CustomAssertionError as e:
#     print("断言失败:", e.message)