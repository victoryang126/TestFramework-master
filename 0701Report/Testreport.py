import time

from BS4ReportUtil2 import *


def test():
    HTMLReport.test_step_aria([False,"None","3344","5566"])

def test2():
    test()

if __name__=="__main__":
    # 创建HTMLReportGenerator实例
    HTMLReport.init()

    # 添加测试类
    HTMLReport.add_test_case('TestCase1')

    # 添加测试步骤数据
    HTMLReport.add_test_group('Testgroup1')
    # time.sleep(1)
    Expect1 = bytearray([i for i in range(100)])
    Actual1 = bytearray([i for i in range(100)])
    # Expect1 = [i for i in range(100)]
    # Actual1 = [i for i in range(100)]
    Actual1[1] = 10
    test()
    test2()
    HTMLReport.test_step_customize_result("Action 1", Actual1, Expect1, True,"This is a test")
    HTMLReport.test_comment("A")
    HTMLReport.test_step_aria([False,"None","3344","5566"])
    HTMLReport.test_step_aria([True, "None", "3344", "5566"])
    Actual1[1] = 20
    HTMLReport.test_step_customize_result('Action 2', Actual1, Expect1, False,["Test Failed"])

    HTMLReport.add_test_group('Testgroup2')
    # time.sleep(5)
    HTMLReport.test_step_customize_result('Action 1', 'Expect 1', 'Actual 1', True)
    HTMLReport.test_step_customize_result('Action 2', 'Expect 2', 'Actual 2', True)

    # print(AriaLog.get_f_back_log(0, "4"))
    # 生成报告
    HTMLReport._end_test_case()
    HTMLReport.generate_report()



