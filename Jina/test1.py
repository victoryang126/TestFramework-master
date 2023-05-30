from jinja2 import Environment, PackageLoader
import datetime

def generate_report(test_data):
    env = Environment(loader=PackageLoader('your_package_name', 'templates'))
    template = env.get_template('report_template.html')

    # 计算测试用例数量、通过数、失败数、跳过数
    test_case_count = len(test_data)
    passed_cases = [t for t in test_data if t['status'] == 'passed']
    failed_cases = [t for t in test_data if t['status'] == 'failed']
    skipped_cases = [t for t in test_data if t['status'] == 'skipped']

    passed_count = len(passed_cases)
    failed_count = len(failed_cases)
    skipped_count = len(skipped_cases)

    # 计算测试总结信息
    start_time = test_data[0]['timestamp']
    end_time = test_data[-1]['timestamp']
    elapsed_time = (end_time - start_time).total_seconds()
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # 生成报告内容
    report_dict = {
        'timestamp': timestamp_str,
        'test_case_count': test_case_count,
        'passed_count': passed_count,
        'failed_count': failed_count,
        'skipped_count': skipped_count,
        'elapsed_time': round(elapsed_time, 2),
        'test_data': test_data
    }

    # 通过Jinja2模板来生成HTML报告
    report_html = template.render(report=report_dict)
    return report_html


import datetime
from unittest.mock import MagicMock, patch

def test_generate_report():
    # 构造测试数据
    test_data = [
        {'name': 'test_1', 'status': 'passed', 'timestamp': datetime.datetime(2023, 5, 30, 12, 0, 0)},
        {'name': 'test_2', 'status': 'failed', 'timestamp': datetime.datetime(2023, 5, 30, 12, 5, 0)},
        {'name': 'test_3', 'status': 'skipped', 'timestamp': datetime.datetime(2023, 5, 30, 12, 10, 0)}
    ]

    # 创建模拟模板
    template_mock = MagicMock()
    template_mock.render.return_value = "<html><body>Test report</body></html>"

    # 模拟装载器和环境
    loader_mock = MagicMock()
    loader_mock.get_template.return_value = template_mock

    env_mock = MagicMock()
    env_mock.loader = loader_mock

    with patch('your_package_name.generate_report.datetime') as datetime_mock:
        # 模拟当前日期时间
        datetime_mock.datetime.now.return_value.strftime.return_value = "2023-05-30 12:15:00.000000"

        # 调用被测函数
        report_html = generate_report(test_data)

        # 验证模板被渲染
        loader_mock.get_template.assert_called_once_with('report_template.html')
        template_mock.render.assert_called_once_with(report={
            'timestamp': '2023-05-30 12:15:00.000000',
            'test_case_count': 3,
            'passed_count': 1,
            'failed_count': 1,
            'skipped_count': 1,
            'elapsed_time': 600.0,
            'test_data': test_data
        })

    # 验证报告正确生成
    assert report_html == "<html><body>Test report</body></html>"

test_generate_report()