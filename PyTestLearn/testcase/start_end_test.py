import pytest

# import py_test
from Draft.PyTestLearn.common.common_util import CommonUtil

"""
pytest-html 生成html报告
pytest-ordering 改变用例执行顺序
pytest-rerunfailres 失败案例重新跑
allure-pytest 生成美观自定义的allure报告
pyYAML 数据对象测试


默认测试用例的规则以及基础应用
1. 模块名必须以test_开头或者_test结尾
2. 测试类必须以Test开头，并且不能带有init方法
3。测试用例必须以test_开头

执行
1. 通过命令行方式运行
2. 通过主函数main方式执行
-vs -V 输出详细信息，-S输出调试信息
-n 多线程运行
--reruns 失败重跑
--html 生成测试报告
-m 指定标记的用例
-k 运行测试用例民初中包含某个字符串的测试用例
3. 通过全局配置文件pytest.ini文件
一般放在项目跟目录下面，必须是pytest.ini
可以更改默认的测试用例规则
[pytest]
addopts = -vs
testpaths = 测试用例路径

python_files = *_test.py 以_test结尾的的
python_classs = Test*
python_functions = test_*
#测试用例分组执行
markers = 
    smoke:冒烟用例

"""

class Test_Class2(CommonUtil):
    workage = 8

    # def setup_class(self):
    #     print("execute before each class")
    #
    # def teardown_class(self):
    #     print("execute after each class")
    #
    # def setup(self):
    #     print("execute before each test case")
    #
    # def teardown(self):
    #     print("execute after each test case")


    def test_1(self):
        print("###Test 1")


    def test_2(self):
        print("####Test 2")


    def test_3(self):
        print("#####Tet 3")

    def test_4(self):
        print("#####Tet 4")


def func(x):
    return x + 1



if __name__ == "__main__":
    #运行所以测试用例
    # pytest.main()
    #输出调试信息
    # pytest.main(['-s'])
    # #指定模块 中标记为smoke的测试用例
    pytest.main(['-sv', 'start_end_test.py', '--html=./report/start_end_test.html', '--self-contained-html'])
