# your_test_file.py
import pytest
from contest import pytest_configure, pytest_runtest_protocol, pytest_unconfigure

@pytest.mark.usefixtures("pytest_configure", "pytest_runtest_protocol", "pytest_unconfigure")
class TestClass:
    def test_function1(self):
        # 测试函数1的代码
        pass

    def test_function2(self):
        # 测试函数2的代码
        pass
