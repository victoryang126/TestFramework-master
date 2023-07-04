import time

from BS4ReportUtil import *


if __name__=="__main__":
    # 创建HTMLReportGenerator实例
    report_generator = HTMLReport()

    # 添加测试类
    report_generator.add_test_case('TestCase1')

    # 添加测试步骤数据
    report_generator.add_test_group('Testgroup1')
    # time.sleep(1)
    Expect1 = [i for i in range(100)]
    Actual1 = [i for i in range(100)]
    Actual1[1] = 10
    report_generator.customize_test_step("Action 1", Actual1, Expect1, HTMLReport.passed)
    report_generator.test_comment("A")
    Actual1[1] = 20
    report_generator.customize_test_step('Action 2', Actual1, Expect1, HTMLReport.failed)
    report_generator.test_comment("C")
    report_generator.test_comment("D")
    report_generator.add_test_group('Testgroup2')
    # time.sleep(5)
    report_generator.customize_test_step('Action 1', 'Expect 1', 'Actual 1', HTMLReport.passed)
    report_generator.customize_test_step('Action 2', 'Expect 2', 'Actual 2', HTMLReport.passed)

    # 生成报告
    report_generator._end_test_case()
    report_generator.generate_report()



