import time

from BS4ReportUtil import *


def test():
    report_generator.test_step_aria([False,"None","3344","5566"])

def test2():
    test()

if __name__=="__main__":
    # 创建HTMLReportGenerator实例
    report_generator = HTMLReport()

    # 添加测试类
    report_generator.add_test_case('TestCase1')

    # 添加测试步骤数据
    report_generator.add_test_group('Testgroup1')
    # time.sleep(1)
    Expect1 = bytearray([i for i in range(100)])
    Actual1 = bytearray([i for i in range(100)])
    # Expect1 = [i for i in range(100)]
    # Actual1 = [i for i in range(100)]
    Actual1[1] = 10
    test()
    test2()
    report_generator.test_step_customize_result("Action 1", Actual1, Expect1, True,"This is a test")
    report_generator.test_comment("A")
    report_generator.test_step_aria([False,"None","3344","5566"])
    report_generator.test_step_aria([True, "None", "3344", "5566"])
    Actual1[1] = 20
    report_generator.test_step_customize_result('Action 2', Actual1, Expect1, False,["Test Failed"])

    report_generator.add_test_group('Testgroup2')
    # time.sleep(5)
    report_generator.test_step_customize_result('Action 1', 'Expect 1', 'Actual 1', True)
    report_generator.test_step_customize_result('Action 2', 'Expect 2', 'Actual 2', True)

    # print(AriaLog.get_f_back_log(0, "4"))
    # 生成报告
    report_generator._end_test_case()
    report_generator.generate_report()



