import datetime

import pytest
import logging




def print_html_table(data):
    # 构建HTML表格
    table = "<html><table>"
    for row in data:
        table += "<tr>"
        for cell in row:
            table += "<td>{}</td>".format(cell)
        table += "</tr>"
    table += "</table></html>"

    # 打印HTML表格
    print(table)

# 示例数据
data = [
    ['Header 1', 'Header 2', 'Header 3'],
    ['Value 1', 'Value 2', 'Value 3'],
    ['Value 4', 'Value 5', 'Value 6']
]

# 打印HTML表格

def test_addition():
    print_html_table(data)

def test_subtraction():
    print(12234)
    assert 5 - 1 == 2
    assert 5 - 2 == 2

def test_not():
    print(1)

@pytest.mark.servername(server='my_server_name')
def test_function():
    print("111")

class Test_C():

    def test_example(self,test_step):
        test_step("Action 1", "Expect 1", "Actual 1")
        print("This is a test")
        test_step("Action 2", "Expect 2", "Actual 2")

    def test_another_example(self,test_step):
        test_step("Action 3", "Expect 3", "Actual 3")
        test_step("Action 4", "Expect 4", "Actual 4")
        # assert result == 'Failed'

if __name__ == "__main__":
    pytest.main(['-v','pytest_hook.py'  ,'--html=test_report_hook.html','--self-contained-html'])
