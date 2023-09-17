
from bs4 import BeautifulSoup

def get_style_and_script(html_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first <style> tag
    style_tag = soup.find('style')
    style = style_tag.string if style_tag else ''

    # Find the first <script> tag
    script_tag = soup.find('script')
    script = script_tag.string if script_tag else ''

    return style, script


class HTMLReportGenerator:
    def __init__(self):
        self.soup = BeautifulSoup(features="html.parser")

    def create_html_structure(self):
        self.html = self.soup.new_tag('html')
        self.soup.append(self.html)

    def create_head_section(self):
        head = self.soup.new_tag('head')
        self.html.append(head)

        meta = self.soup.new_tag('meta', charset='utf-8')
        head.append(meta)

        title = self.soup.new_tag('title')
        title.string = 'pytestReport'
        head.append(title)

        template_style,template_script = get_style_and_script("template.html")

        style = self.soup.new_tag('style')
        style.string = template_style
        head.append(style)

        script_tag = self.soup.new_tag('script')
        script_tag.string = template_script
        head.append(script_tag)

    def create_body_section(self):
        self.body = self.soup.new_tag('body', onLoad='init()')
        self.html.append(self.body)

    def add_title(self, title_text):
        h1 = self.soup.new_tag('h1')
        h1.string = title_text
        self.body.append(h1)

    def add_timestamp(self, timestamp_text):
        timestamp = self.soup.new_tag('p')
        timestamp.string = timestamp_text
        self.body.append(timestamp)

    def add_environment_section(self, environment_data):
        h2_env = self.soup.new_tag('h2')
        h2_env.string = 'Environment'
        self.body.append(h2_env)

        env_table = self.soup.new_tag('table', id='environment')
        self.body.append(env_table)

        for key, value in environment_data.items():
            tr = self.soup.new_tag('tr')
            env_table.append(tr)

            td1 = self.soup.new_tag('td')
            td1.string = key
            tr.append(td1)

            td2 = self.soup.new_tag('td')
            td2.string = value
            tr.append(td2)

    def add_summary_section(self):
        h2_summary_section = self.soup.new_tag('h2')
        h2_summary_section.string = 'Summary'

        self.body.append(h2_summary_section)

        summary_table = self.soup.new_tag('table', id='testcasesSummaryTable')
        self.body.append(summary_table)

        headers = ['Category', 'Count', 'Show/Hide']
        header_row = self.soup.new_tag('tr')
        summary_table.append(header_row)
        for header in headers:
            th = self.soup.new_tag('th')
            th.string = header
            header_row.append(th)

        data = [
            ('Total test cases:', 'total', ''),
            ('Failed test cases:', 'Failed', 'Failed'),
            ('Passed test cases:', 'Passed', 'Passed')
        ]
        for item in data:
            category, count_id, checkbox_label = item
            tr = self.soup.new_tag('tr')
            summary_table.append(tr)

            td1 = self.soup.new_tag('td')
            td1.string = category
            tr.append(td1)

            td2 = self.soup.new_tag('td', id=count_id)
            tr.append(td2)

            td3 = self.soup.new_tag('td')
            tr.append(td3)

            if checkbox_label:
                checkbox = self.soup.new_tag('input', type='checkbox', checked=True, onclick=f"toggletestcaseRowVisibility('{checkbox_label}')")
                td3.append(checkbox)



    def add_results_section(self):
        results_section = self.soup.new_tag('h2')
        results_section.string = 'Results'
        self.body.append(results_section)

        results_table = self.soup.new_tag('table', id='results-table')
        self.body.append(results_table)
        # results_section.insert_after(results_table)

        thead = self.soup.new_tag('thead', id='results-table-head')
        results_table.append(thead)

        headers = ['Timestamp', 'Test Class', 'Result', 'Duration (s)']
        header_row = self.soup.new_tag('tr')
        thead.append(header_row)
        for header in headers:
            th = self.soup.new_tag('th', col=header.lower().replace(' ', '-'))
            th.string = header
            header_row.append(th)

    def generate_report(self, file_path):
        with open(file_path, 'w') as file:
            file.write(self.soup.prettify())


# Example usage:
report_generator = HTMLReportGenerator()
report_generator.create_html_structure()
report_generator.create_head_section()
report_generator.create_body_section()
report_generator.add_title('bsreport')
report_generator.add_timestamp('03-Jun-2023 17:46:00')
environment_data = {'Browser': 'Chrome', 'OS': 'Windows'}
report_generator.add_environment_section(environment_data)
summary_data = [('TestClassA', 'testcase1', 'tcRow1'), ('TestClassB', 'testcase2', 'tcRow2')]
report_generator.add_summary_section()
results_data = [
    ('03-Jun-2023 17:46:00', 'TestClassA', 'Passed', '0.132s'),
    ('03-Jun-2023 17:46:02', 'TestClassB', 'Failed', '2.781s'),
    ('03-Jun-2023 17:46:05', 'TestClassC', 'Passed', '1.645s')
]
report_generator.add_results_section()
report_generator.generate_report('report.html')
