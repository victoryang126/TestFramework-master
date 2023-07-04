
import pytest
from ReportUtil import Result,Report
import inspect

@pytest.fixture(scope='class',autouse=True)
def setup_testclass(request):
    test_class_name = request.node.nodeid
    Result.add_test_class(test_class_name)
    # yield
    # Result.end_test_class()



@pytest.fixture(scope='function',autouse=True)
def setup_test(request):
    # 在测试函数之前执行的代码
    test_class_name = request.node.nodeid
    Result.add_test_case(test_class_name)
    # yield  # yield 语句将分隔在测试函数之前和之后执行的代码
    # Result._end_test_case()


class TestExample:

    def test_case_1(self):
        Expect1 = [i for i in range(100)]
        Actual1 = [i for i in range(100)]
        Actual1[1] = 10
        print(Actual1[1])
        try:
            assert Expect1 == Actual1
            result = [Result.passed,None]
        except AssertionError as e:
            result = [Result.failed,str(e)]
        Result.test_step2("compare Expect1 euqla Actual1",Expect1,Actual1,result)
        Actual1[1] = 20
        Result.test_comment("Waaaa")
        print(Actual1[1])
        try:
            assert Expect1 == Actual1
            result = [Result.passed,None]
        except AssertionError as e:
            result = [Result.failed,str(e)]
        Result.test_step2("compare Expect2 euqla Actual2",Expect1,Actual1,result)

        # Result._end_test_case()

    def test_case_2(self):
        Expect1 = "0x5010003201f4"
        Actual1 = "0x5010003201F"
        # Actual1[1] = 10
        try:
            assert Expect1 == Actual1
            result = [Result.passed,None]
        except AssertionError as e:
            result = [Result.failed,str(e)]
        Result.test_step2("compare Expect1 euqla Actual1",Expect1,Actual1,result)
        Result.end_test_case()
        Result.end_test_class()


if __name__ == "__main__":
    pytest.main(['-v','test2.py'  ,'--html=test.html','--self-contained-html'])
    # pytest.main(['-vs','test.py','--html=test.html','--self-contained-html'])
    # pytest.main(['-v','test.py','--show-capture=no'])
    report = Report()
    report.generate_html(Result.results,"test_report2.html")
