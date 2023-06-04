import pytest
# from common.common_util import CommonUtil
# import pytest_html


if __name__ == "__main__":
    pytest.main(['-sv', './testcase/Different_options_for_test_IDs.py', '--html=./report/Different_options_for_test_IDs.html', '--self-contained-html'])
    #运行所以测试用例
    # pytest.main()
    #输出调试信息
    # pytest.main(['-s'])
    # #指定模块 中标记为smoke的测试用例
    # pytest.main(['-sv', '-m=smoke', './testcase', '--html=./report/result.html', '--self-contained-html'])
    # pytest.main(['-sv','./testcase/py_test.py','--html=./report/py_test.html','--self-contained-html'])
    # #指定文件夹
    # pytest.main(['-sv','./testcase'])
    #
    # #指定nodeid 运行特定模块中的某个用例::python分隔符
    # pytest.main(['-sv', './testcase/py_test.py::Test_Class::test_1'])
    # pytest.main(["--html ./report/report.html"])
    # pytest.main(["-vs --html=./report/result.html"])
    # pytest.main()