from jinja2 import Environment, FileSystemLoader

# 准备模板环境
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# 准备数据
data = {
    'title': 'Report 20230601',
    'report_title': 'report20230601.html',
    'generated_date': '30-May-2023 at 22:31:09',
    'machine': 'MonsterdeMacBook-Pro.local',
    'user': 'monster',
    'results': [
        {
            'time': '2023-05-30 22:31:09.590726',
            'test_class': '-',
            'result': {
                'status': 'Passed',
                'test': 'pytest_hook.py::Test_C::test_example',
                'duration': '0.00',
            },
            'test_cases': [
                {
                    'timestamp': 'Timestamp 2',
                    'test_case': 'TestCase 1',
                    'file': 'File 2',
                    'duration': 'Duration 2',
                    'status': 'Passed',
                    'test_steps': [
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 3',
                            'action': 'Action 3',
                            'expect': 'Expect 3',
                            'actual': 'Actual 3',
                            'status': 'Result 3',
                            'step_status': 'Passed'
                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status': 'Result 4',
                            'step_status': 'Passed'
                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status': 'Result 4',
                            'step_status': 'Passed'
                        }
                    ]
                }
            ]
        },
        {
            'time': '2023-05-30 22:31:09.590936',
            'test_class': '-',
            'result': {
                'status': 'Failed',
                'test': 'pytest_hook.py::Test_C::test_another_example',
                'duration': '0.00',
            },
            'test_cases': [
                {
                    'timestamp': 'Timestamp 2',
                    'test_case': 'TestCase 3',
                    'file': 'File 2',
                    'duration': 'Duration 2',
                    'status': 'Failed',
                    'test_steps': [
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 3',
                            'action': 'Action 3',
                            'expect': 'Expect 3',
                            'actual': 'Actual 3',
                            'status': 'Result 3',
                            'step_status': 'Passed'
                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status': 'Result 4',
                            'step_status': 'Failed'
                        }
                    ]
                }
            ]
        }
    ]
}

# 渲染模板并生成HTML
output = template.render(data)

# 将HTML写入文件
with open('report.html', 'w') as file:
    file.write(output)
