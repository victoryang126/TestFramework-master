from bs4 import BeautifulSoup

class TestReportGenerator:
    def __init__(self):
        self.template_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report</title>
        </head>
        <body>
            <table id="results-table">
                <tr><th>Results</th></tr>
            </table>
            <table class="test_cases">
                <tr><th>Test Cases</th></tr>
            </table>
            <table class="test_steps">
                <tr><th>Test Steps</th></tr>
            </table>
        </body>
        </html>
        """
        self.results_table = None
        self.test_cases_table = None
        self.test_steps_table = None

    def initialize_html(self):
        self.results_table = BeautifulSoup("<tr></tr>", 'html.parser').tr
        self.test_cases_table = BeautifulSoup("<tr></tr>", 'html.parser').tr
        self.test_steps_table = BeautifulSoup("<tr></tr>", 'html.parser').tr

    def add_row_to_results(self, row_data):
        row = BeautifulSoup("<tr></tr>", 'html.parser').tr
        for data in row_data:
            cell = BeautifulSoup(f"<td>{data}</td>", 'html.parser').td
            row.append(cell)
        self.results_table.append(row)

    def add_test_case(self, test_case):
        row = BeautifulSoup("<tr></tr>", 'html.parser').tr
        cell = BeautifulSoup(f"<td>{test_case}</td>", 'html.parser').td
        row.append(cell)
        self.test_cases_table.append(row)

    def add_test_step(self, test_step):
        row = BeautifulSoup("<tr></tr>", 'html.parser').tr
        cell = BeautifulSoup(f"<td>{test_step}</td>", 'html.parser').td
        row.append(cell)
        self.test_steps_table.append(row)

    def generate_html(self, filename):
        html = BeautifulSoup(self.template_html, 'html.parser')
        html.find('table', id='results-table').replace_with(self.results_table)
        html.find('table', class_='test_cases').replace_with(self.test_cases_table)
        html.find('table', class_='test_steps').replace_with(self.test_steps_table)
        with open(filename, 'w') as file:
            file.write(html.prettify())

# 示例用法
report_generator = TestReportGenerator()
report_generator.initialize_html()

# 添加行和数据
report_generator.add_row_to_results(['Result 1', 'Pass'])
report_generator.add_row_to_results(['Result 2', 'Fail'])
report_generator.add_test_case('Test Case 1')
report_generator.add_test_case('Test Case 2')
report_generator.add_test_step('Step 1')
report_generator.add_test_step('Step 2')

# 生成HTML文档并保存为文件
report_generator.generate_html('report.html')
