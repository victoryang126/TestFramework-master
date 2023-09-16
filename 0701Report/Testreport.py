# SWV_Generic_Lib.py
class G_Var:
    var1 = None
    var2 = None

class SWV_Generic_Lib:
    @classmethod
    def some_function(cls):
        # 使用G_Var类属性中的全局变量
        print(f"var1: {G_Var.var1}, var2: {G_Var.var2}")

# Project_Lib.py
# from SWV_Generic_Lib import SWV_Generic_Lib

class Project_Lib(SWV_Generic_Lib):
    pass
    # @staticmethod
    # def another_static_function():
    #     # 在这里可以调用父类的方法
    #     SWV_Generic_Lib.some_function()

# # 在另一个文件或测试脚本中：
# from SWV_Generic_Lib import G_Var
# from Project_Lib import Project_Lib

# 直接通过类名修改G_Var的属性
G_Var.var1 = "New Value for var1"
G_Var.var2 = "New Value for var2"

# 直接通过类名调用Project_Lib中的方法
Project_Lib.some_function()
