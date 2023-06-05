import socket
import getpass
import pytest
from datetime import datetime
from py.xml import html


G_TestSteps = []

def asset_and_return(condition):
    try:
        assert condition
        return True
    except AssertionError:
        # raise AssertionError
        return False

class Result:
    passed = "Passed"
    failed = "Failed"
    tbd = "TBD"

@pytest.fixture(scope="session", autouse=True)
def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

@pytest.fixture(scope="function", autouse=True)
def test_step(request, timestamp):

    count = 1  # 步骤计数器

    def save_test_steps(action, expect_result, actual_result):
        nonlocal count  # 使用非本地变量
        result = Result.tbd
        ret = asset_and_return(expect_result == actual_result)
        # assert expect_result == actual_result
        if ret:
            result = Result.passed
        else:
            result = Result.failed
        test_step = {
            'Timestamps': timestamp,
            'Step': count,
            'Action': action,
            'Expect': expect_result,
            'Actual': actual_result,
            'Result': result
        }
        count += 1  # 计数器递增
        G_TestSteps.append(test_step)

    yield save_test_steps

    # if hasattr(request.node, 'test_table'):
    #     test_table = request.node.test_table
    #     print(test_table)



def pytest_configure(config):
    # 获取机器名
    machine_name = socket.gethostname()
    # 获取用户名
    username = getpass.getuser()
    # 设置报告的元数据
    config._metadata =  {
        "Machine": machine_name,
        "User": username,
    }
    # config._metadata['Machine'] = machine_name
    # config._metadata['User'] = username


# def pytest_html_results_table_header(cells):
#     cells.insert(0, html.th('Time', class_='sortable time', col='time'))
#     # if hasattr(report, "server_name"):
#     cells.insert(1, html.th('Server Name', class_='sortable server-name', col='server-name'))
#     cells.pop()

def pytest_html_results_table_header(cells):
    cells.insert(0, html.th('Time', col='time'))
    # if hasattr(report, "server_name"):
    cells.insert(1, html.th('Server Name', col='server-name'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(0, html.td(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), class_='col-time'))
    if hasattr(report, "server_name"):
        cells.insert(1, html.td(report.server_name, class_='col-server-name'))
    else:
        cells.insert(1, html.td("-",class_='col-server-name'))
    cells.pop()



def generate_html_table():
    html = '''
    <p>
    <style>
         table {
          border-collapse: collapse;
          width: 100%;
          background-color: #f2f2f2;
       }

        th, td {
          border: 1px solid #ddd;
          padding: 8px;
          text-align: left;
       }

       #test_steps th {
          #background-color: #FFF5EE;
          color: #000000;
       }

       tr.pass {
          background-color: #c9ecc9;
       }

       tr.fail {
          background-color: #f8caca;
       }

       tr.tbd {
          background-color: #fdfdc4;
       }
    </style>
    <table id="test_steps">
      <tr>
        <th>Timestamps</th>
        <th>TestSteps</th>
        <th>Action</th>
        <th>Expect</th>
        <th>Actual</th>
        <th>Result</th>
      </tr>
    </table>
    </p>
    '''
    return html


def generate_html_table2():
    html = '''
        <p>
        <style>
             table {
              border-collapse: collapse;
              width: 100%;
              background-color: #f2f2f2;
           }

            th, td {
              border: 1px solid #ddd;
              padding: 8px;
              text-align: left;
           }

           #test_steps th {
              #background-color: #FFF5EE;
              color: #000000;
           }

           tr.pass {
              background-color: #c9ecc9;
           }

           tr.fail {
              background-color: #f8caca;
           }

           tr.tbd {
              background-color: #fdfdc4;
           }
        </style>
        <table id="test_steps">
          <tr>
            <th>Timestamps</th>
            <th>TestSteps</th>
            <th>Action</th>
            <th>Expect</th>
            <th>Actual</th>
            <th>Result</th>
          </tr>
    '''

    for item in G_TestSteps:
        result_class = ''
        if item['Result'] == 'TBD':
            result_class = 'tbd'
        elif item['Result'] == 'Passed':
            result_class = 'pass'
        elif item['Result'] == 'Failed':
            result_class = 'fail'

        html += f'''
            <tr class="{result_class}">
                <td>{item['Timestamps']}</td>
                <td>{item['Step']}</td>
                <td>{item['Action']}</td>
                <td>{item['Expect']}</td>
                <td>{item['Actual']}</td>
                <td>{item['Result']}</td>
            </tr>
        '''

    html += '''
        </table>
        </p>
    '''

    return html



# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#     if report.when == 'call':
#         #默认的stdout暂时不知道如何删除
#         extra.append(pytest_html.extras.html(generate_html_table()))
#         report.extra = extra

@pytest.hookimpl(hookwrapper=True)
# @pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    if 'servername' in item.keywords:
        report.server_name = item.keywords['servername'].kwargs['server']
    else:
        report.server_name = "-"

    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        #默认的stdout暂时不知道如何删除
        extra.append(pytest_html.extras.html(generate_html_table2()))
        report.extra = extra
