import pytest
from collections import defaultdict

# 自定义的测试结果收集器
class CustomTestResult:
    def __init__(self):
        self.results = defaultdict(lambda: defaultdict(list))

    def add_result(self, test_class, test_case, test_step, result):
        self.results[test_class][test_case].append((test_step, result))

    def get_failures(self):
        failures = []
        for test_class, test_cases in self.results.items():
            class_failed = False
            for test_case, test_steps in test_cases.items():
                case_failed = False
                for step, result in test_steps:
                    if result == "fail":
                        case_failed = True
                        class_failed = True
                        failures.append((test_class, test_case, step))
                if case_failed:
                    failures.append((test_class, test_case, "test case failed"))
            if class_failed:
                failures.append((test_class, "test class failed"))
        return failures

# pytest钩子函数，收集测试结果
def pytest_runtest_makereport(item, call):
    result = None
    if call.excinfo is not None:
        result = "fail"
    elif call.when == "call":
        result = "pass"
    if result is not None:
        test_class = item.cls.__name__ if item.cls else "NoClass"
        test_case = item.name
        test_step = call.when
        custom_result.add_result(test_class, test_case, test_step, result)

# 自定义的pytest插件
class CustomReportPlugin:
    def pytest_sessionstart(self, session):
        global custom_result
        custom_result = CustomTestResult()

    def pytest_sessionfinish(self, session):
        failures = custom_result.get_failures()
        if failures:
            print("Custom Test Report:")
            for failure in failures:
                print(failure)

# 在pytest配置文件中注册自定义插件
def pytest_configure(config):
    config.pluginmanager.register(CustomReportPlugin())

# 测试用例示例
class TestExample:
    def test_case_1(self):
        assert True

    def test_case_2(self):
        assert False

    def test_case_3(self):
        assert True

    def test_case_4(self):
        assert True

    def test_case_5(self):
        assert False


if __name__ == "__main__":
    pytest.main(["-qq"])
    # pytest.main(['-v','test.py'  ,'--html=test.html','--self-contained-html'])
