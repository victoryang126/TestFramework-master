from jinja2 import Environment, FileSystemLoader

# 1. 准备模板环境
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# 2. 准备数据
data = {
    'title': 'Report 20230601',
    'report_title': 'report20230601.html',
    'generated_date': '30-May-2023 at 22:31:09',
    'machine': 'MonsterdeMacBook-Pro.local',
    'user': 'monster',
    'results': [
        {
            'time': '2023-05-30 22:31:09.590726',
            'test_class': 'AA',
            'result': 'Passed',
            'test': 'pytest_hook.py::Test_C::test_example',
            'status':"passed",
            'duration': '0.00',
            'test_cases': [
                {
                    'timestamp': 'Timestamp 2',
                    'test_case': 'TestCase 1',
                    'file': 'File 2',
                    'duration': 'Duration 2',
                    'result': 'Passed',
                    'status':"passed",
                    'test_steps': [
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 3',
                            'action': 'Action 3',
                            'expect': 'Expect 3',
                            'actual': 'Actual 3',
                            'status':"failed",
                            'result': 'Failed'
                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status':"passed",
                            'result': 'Passed'
                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status':"failed",
                            'result': 'Failed'
                        }
                    ]
                }
            ]
        },
        {
            'time': '2023-05-30 22:31:09.590936',
            'test_class': 'BB',
            'result': 'Failed',
            'test': 'pytest_hook.py::Test_C::test_another_example',
            'duration': '0.00',
            'status':"passed",
            'test_cases': [
                {
                    'timestamp': 'Timestamp 2',
                    'test_case': 'TestCase 3',
                    'file': 'File 2',
                    'duration': 'Duration 2',
                    'result': 'Failed',
                    'status':"failed",
                    'test_steps': [
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 3',
                            'action': 'Action 3',
                            'expect': 'Expect 3',
                            'actual': 'Actual 3',
                            'status':"passed",
                            'result': 'Result 3'

                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status':"tbd",
                            'result': 'Result 4'
                        },
                        {
                            'timestamp': 'Timestamp 2',
                            'test_step': 'TestSteps 4',
                            'action': 'Action 4',
                            'expect': 'Expect 4',
                            'actual': 'Actual 4',
                            'status':"failed",
                            'result': 'Result 4'
                        }
                    ]
                }
            ]
        }
    ]
}

# 3. 渲染模板并生成HTML
output = template.render(data)

# 4. 将HTML写入文件
with open('report.html', 'w') as file:
    file.write(output)
