# 默认的钩子函数
def default_hook():
    """they are"""
    print("Default hook executed!")

# 全局变量存储当前的钩子
hook_function = default_hook

# 允许用户设置自己的钩子
def set_hook(func):
    global hook_function
    hook_function = func

# 当某事件发生时，调用这个钩子
def trigger_event():
    hook_function()

# 用户定义的钩子
def custom_hook():
    """
    this is
    :return:
    """
    print("Custom hook executed!")

# 设置用户的钩子
set_hook(custom_hook)

# 触发事件
# trigger_event()  # 输出: "Custom hook executed!"
hook_function()


class Config:
    VAR_1 = "default_value1"
    VAR_2 = "default_value2"


Config.VAR_2 = 3

def test():
    print(Config.VAR_2)


test()