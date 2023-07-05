import inspect
import traceback
import sys

class MyLogger:
    def log(self, message):
        frame_info = inspect.currentframe().f_back
        line_number = frame_info.f_lineno
        file_name = frame_info.f_code.co_filename
        print(f"Log message: {message}, called at line {line_number} in file {file_name}")
        # exc_type,exc_value,exe_traceback_obj = sys.exc_info()
        # print(exc_type,exc_value,exe_traceback_obj)

# 示例调用
logger = MyLogger()
logger.log("Hello, world!")

# f_back：指向调用当前帧的帧对象。
#
# f_code：表示当前帧正在执行的代码对象。
#
# f_locals：表示当前帧的局部命名空间。
#
# f_globals：表示当前帧的全局命名空间。
#
# f_lineno：表示当前帧的代码行号。
#
# f_trace：设置为一个跟踪函数（trace function），用于跟踪代码的执行。

def foo():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    code_object = caller_frame.f_code
    local_variables = caller_frame.f_locals
    global_variables = caller_frame.f_globals
    line_number = caller_frame.f_lineno
    trace_function = caller_frame.f_trace

    print("Code object:", code_object)
    print("Local variables:", local_variables)
    print("Global variables:", global_variables)
    print("Line number:", line_number)
    print("Trace function:", trace_function)

foo()
