from abc import ABC, abstractmethod

class MyInterface(ABC):

    @abstractmethod
    def method1(self):
        pass

    @abstractmethod
    def method2(self):
        pass

class MyClass(MyInterface):

    def method1(self):
        print("Implementing method1")

    def method2(self):
        print("Implementing method2")

# # 示例使用
# obj = MyClass()
# obj.method1()  # 输出: Implementing method1
# obj.method2()  # 输出: Implementing method2
#

def library_function(callback_function):
    # 使用回调函数进行操作
    result = callback_function()
    # 其他库函数的代码逻辑

def user_defined_function():
    # 用户自定义的函数逻辑
    return "A,B"

# 使用库函数并传递用户定义的函数
library_function(user_defined_function)

global_variable = "some_value"

def library_function():
    # 使用全局变量进行操作
    global global_variable
    result = global_variable
    # 其他库函数的代码逻辑

# 使用库函数
library_function()

def get_attributes_and_methods_from_file(file_path):
    # 导入指定文件作为模块
    import importlib.util
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 获取属性和方法列表
    attributes = []
    methods = []

    for item_name in dir(module):
        item = getattr(module, item_name)
        if callable(item):
            methods.append(item_name)
        else:
            attributes.append(item_name)

    return attributes, methods

