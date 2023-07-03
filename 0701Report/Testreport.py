import time

from BS4ReportUtil import *


if __name__=="__main__":
    # 创建HTMLReportGenerator实例
    report_generator = HTMLReportGenerator()

    # 添加测试类
    report_generator.add_test_case('TestCase1')

    # 添加测试步骤数据
    report_generator.add_test_group('Testgroup1')
    time.sleep(1)
    report_generator.add_test_step('Step 1', 'Action 1', 'Expect 1', 'Actual 1', HTMLReportGenerator.passed)
    report_generator.add_test_step('Step 2', 'Action 2', 'Expect 2', 'Actual 2', HTMLReportGenerator.failed)

    report_generator.add_test_group('Testgroup2')
    time.sleep(0.5)
    report_generator.add_test_step('Step 1', 'Action 1', 'Expect 1', 'Actual 1', HTMLReportGenerator.passed)
    report_generator.add_test_step('Step 2', 'Action 2', 'Expect 2', 'Actual 2', HTMLReportGenerator.passed)

    # 生成报告
    report_generator.generate_report()

    print("Report generated successfully.")


