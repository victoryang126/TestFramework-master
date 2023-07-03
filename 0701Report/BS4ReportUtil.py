from pathlib import Path
import bs4
from bs4 import BeautifulSoup
import getpass
import socket
import os
import datetime
import copy

from bs4.formatter import HTMLFormatter


class HTMLReportGenerator:

    passed = "Passed"
    failed = "Failed"
    group = 0
    step = 0

    def __init__(self,html_title=None,report_path=""):

        self.test_case_result = self.passed
        self.test_group_result = self.passed

        self.soup = BeautifulSoup(features="html.parser")
        self.html = self.soup.new_tag('html')
        self.soup.append(self.html)

        if html_title == None:
            self.html_title = os.path.basename(__file__).split(".")[0]
        else:
            self.html_title = html_title

        self.report_path = report_path

        file_path = os.path.join(self.report_path, f"{self.html_title}.html")
        self.file = open(file_path, "w")
        self.module_versions = self.get_module_versions()

        self.add_head_section()
        self.add_environment_section()
        self.add_summary_section()
        self.add_results_section()




    def get_machine_name(self):
        return socket.gethostname()

    def get_user(self):
        return getpass.getuser()

    def get_module_versions(self):
        module_version = {}
        module_version["BS4"] = bs4.__version__
        pass
        #TODO get version of related module
        return module_version


    def add_module_versions(self,module_verions:dict):
        """
        function used to update the module_versions
        :param module_verions:
        :return:
        """
        self.module_versions.update(module_verions)

    def get_style_and_script(self,html_file):
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

    def add_head_section(self):
        head = self.soup.new_tag('head')
        self.html.append(head)

        meta = self.soup.new_tag('meta', charset='utf-8')
        head.append(meta)

        title = self.soup.new_tag('title')
        title.string = self.html_title
        head.append(title)

        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "")
        template = os.path.join(template_path,"template.html")
        template_style,template_script = self.get_style_and_script(template)

        style = self.soup.new_tag('style')
        style.string = template_style
        head.append(style)

        self.body = self.soup.new_tag('body', onLoad='init()')
        self.html.append(self.body)

        script_tag = self.soup.new_tag('script')
        script_tag.string = template_script
        self.body.append(script_tag)

        h1 = self.soup.new_tag('h1')
        h1.string = self.html_title
        self.body.append(h1)

        timestamp = self.soup.new_tag('p')

        now = datetime.datetime.now()
        timestamp.string = f"Report Generate at {now.strftime('%Y-%m-%d %H:%M:%S')}"
        self.body.append(timestamp)



    def add_environment_section(self):
        h2_env = self.soup.new_tag('h2')
        h2_env.string = 'Environment'
        self.body.append(h2_env)
        environment_data = {}
        environment_data["User"] = self.get_user()
        environment_data["Machine"] = self.get_machine_name()
        environment_data.update(self.module_versions)
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

        summary_table = self.soup.new_tag('table', id='testgroupsSummaryTable')
        self.body.append(summary_table)

        headers = ['Category', 'Count', 'Show/Hide']
        header_row = self.soup.new_tag('tr')
        summary_table.append(header_row)
        for header in headers:
            th = self.soup.new_tag('th')
            th.string = header
            header_row.append(th)

        data = [
            ('Total test groups:', 'total', ''),
            ('Failed test groups:', 'Failed', 'Failed'),
            ('Passed test groups:', 'Passed', 'Passed')
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
                checkbox = self.soup.new_tag('input', type='checkbox', checked=True, onclick=f"toggletestgroupsRowVisibility('{checkbox_label}')")
                td3.append(checkbox)

    def add_results_section(self):
        results_section = self.soup.new_tag('h2')
        results_section.string = 'Results'
        self.body.append(results_section)

        self.results_table = self.soup.new_tag('table', id='results-table')
        self.body.append(self.results_table)
        # results_section.insert_after(results_table)

        thead = self.soup.new_tag('thead', id='results-table-head')
        self.results_table.append(thead)

        headers = ['Timestamp', 'Test Case', 'Result', 'Duration(s)']
        header_row = self.soup.new_tag('tr')
        thead.append(header_row)
        for header in headers:
            th = self.soup.new_tag('th', col=header.lower().replace(' ', '-'))
            th.string = header
            header_row.append(th)

    def generate_report(self):
        self.file.write(self.soup.prettify(formatter='html5'))
        file_path = os.path.join(self.report_path,f"{self.html_title}.html")
        # # self.report = open(file_path,"w")
        # # self.report.read(self.soup.prettify())
        # with open(file_path, 'w') as file:
        #     file.write(self.soup.prettify(formatter = 'html5')) # if use this kind method, there some problem with the report
        #     # file.write(str(self.html))
        html_report = Path(os.path.expandvars(file_path)).expanduser()
        print(f"generate customize html report: {html_report.absolute().as_uri()}")
        self.file.close()

    def add_test_case(self, test_case):
        self.group = 0
        self.test_case = test_case
        self.test_case_result = self.passed
        self.test_case_body = self.soup.new_tag('tbody')
        self.test_case_row = self.soup.new_tag('tr',attrs={"class": "Passed results-table-row"})
        # Append the row to the results table
        self.test_case_body.append(self.test_case_row)
        self.results_table.append(self.test_case_body)

        self.test_case_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        result = self.test_case_result
        duration = "0.0"
        # Create and append table cells for each column of data
        timestamp_cell = self.soup.new_tag('td')
        timestamp_cell.string = self.test_case_timestamp
        self.test_case_row.append(timestamp_cell)

        test_case_cell = self.soup.new_tag('td')
        test_case_cell.string = test_case
        self.test_case_row.append(test_case_cell)

        result_cell = self.soup.new_tag('td',attrs={"class": "col-result"})
        result_cell.string = result
        self.test_case_row.append(result_cell)

        duration_cell = self.soup.new_tag('td')
        duration_cell.string = duration
        self.test_case_row.append(duration_cell)

        self.add_extra_row_for_test_class()


    def add_extra_row_for_test_class(self):
        # Add the additional row for test cases
        extra_row = self.soup.new_tag('tr')
        self.test_case_body.append(extra_row)

        extra_cell = self.soup.new_tag('td', attrs = {"class":"extra","colspan":"5"})
        extra_row.append(extra_cell)

        div = self.soup.new_tag('div')
        extra_cell.append(div)

        self.test_group_table = self.soup.new_tag('table', attrs = {"class":"test_groups"})
        div.append(self.test_group_table)

        thead = self.soup.new_tag('thead', attrs = {"class":"test_groups_header"})
        self.test_group_table.append(thead)

        thead_row = self.soup.new_tag('tr')
        thead.append(thead_row)

        headers = ['Timestamp', 'TestGroup',  'Result','Duration(s)']
        for header_text in headers:
            th = self.soup.new_tag('th')
            th.string = header_text
            thead_row.append(th)


        # tbody = self.soup.new_tag('tbody')


    def add_test_group(self, test_group):
        self.group += 1
        self.step = 0
        self.test_group_result = self.passed
        # Create a new row for the test case in the test_cases_table
        self.test_group_row = self.soup.new_tag('tr',attrs={"class": "Passed results-table-row"})
        self.test_group_table.append(self.test_group_row)

        self.test_group_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        duration = "0.0"
        result = self.test_group_result

        # Create and append table cells for each column of data
        timestamp_cell = self.soup.new_tag('td')
        timestamp_cell.string = self.test_group_timestamp
        self.test_group_row.append(timestamp_cell)

        test_group_cell = self.soup.new_tag('td')
        test_group_cell.string = f"Group {self.group} {self.test_case}::{test_group}"
        self.test_group_row.append(test_group_cell)


        result_cell = self.soup.new_tag('td',attrs={"class": "col-result"})
        result_cell.string = result
        self.test_group_row.append(result_cell)

        duration_cell = self.soup.new_tag('td')
        duration_cell.string = str(duration)
        self.test_group_row.append(duration_cell)

        # Add the details table with test steps
        details_row = self.soup.new_tag('tr', attrs={"class": "details"})
        self.test_group_table.append(details_row)

        details_cell = self.soup.new_tag('td', colspan='6')
        details_row.append(details_cell)

        self.test_steps_table = self.soup.new_tag('table', attrs={"class": "test_steps"})
        details_cell.append(self.test_steps_table)

        details_thead = self.soup.new_tag('thead')
        self.test_steps_table.append(details_thead)

        details_thead_row = self.soup.new_tag('tr', attrs={"class": "test_step_header"})
        details_thead.append(details_thead_row)

        step_headers = ['Timestamps', 'TestSteps', 'Action', 'Expect', 'Actual', 'Result']
        for step_header in step_headers:
            th = self.soup.new_tag('th')
            th.string = step_header
            details_thead_row.append(th)

        # Add the test steps
        # details_tbody = self.soup.new_tag('tbody')
        # self.test_steps_table.append(details_tbody)

    def add_test_step(self,action, expect, actual, result):

        self.step +=1

        # Create a new row for the test step in the test_steps_table
        attrs={"class": 'Passed' if result == self.passed else 'Failed'}
        test_step_row = self.soup.new_tag('tr', attrs=attrs)
        self.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data
        now = datetime.datetime.now()

        self.update_duration_result_for_testcase_testgroup(now,result)

        timestamp_cell = self.soup.new_tag('td')
        timestamp_cell.string = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        test_step_row.append(timestamp_cell)

        test_step_cell = self.soup.new_tag('td')
        test_step_cell.string = f"Step {self.step}"
        test_step_row.append(test_step_cell)

        action_cell = self.soup.new_tag('td')
        action_cell.append(str(action))
        test_step_row.append(action_cell)

        expect_cell = self.soup.new_tag('td')
        expect_cell.append(str(expect))
        test_step_row.append(expect_cell)

        actual_cell = self.soup.new_tag('td')
        actual_cell.append(str(actual))
        test_step_row.append(actual_cell)

        result_cell = self.soup.new_tag('td',attrs={"class": "col-test-step-log"})
        result_cell.string = result
        test_step_row.append(result_cell)

        self.add_test_log()
          # if use this kind method, there some problem with the report

    def update_report(self):
        self.file.write(self.soup.prettify(formatter='html5'))

    def add_test_log(self):
        log_row = self.soup.new_tag('tr')
        td_colspan = self.soup.new_tag('td',attrs = {"colspan": "6"})
        self.log_div = self.soup.new_tag('div',attrs = {"class": "log"})
        # self.log_div.string = ""
        td_colspan.append(self.log_div)
        log_row.append(td_colspan)
        self.test_steps_table.append(log_row)

    def update_duration_result_for_testcase_testgroup(self,now,result):
        end = datetime.datetime.strptime(now.strftime('%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')
        test_case_start = datetime.datetime.strptime(self.test_case_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        test_group_start = datetime.datetime.strptime(self.test_group_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        test_case_duration =  "{:.4f}".format((end - test_case_start).total_seconds())
        test_case_duration_ele = self.test_case_row.select('td')[3]
        test_case_duration_ele.string = test_case_duration
        test_group_duration = "{:.4f}".format((end - test_group_start).total_seconds())
        test_group_duration_ele = self.test_group_row.select('td')[3]
        test_group_duration_ele.string = test_group_duration

        #update the test result for test case and test group
        if result == self.failed:
            if self.test_case_row['class'] != 'Failed results-table-row':
                self.test_case_row['class'] = 'Failed results-table-row'
            if self.test_group_row['class'] != 'Failed results-table-row':
                self.test_group_row['class'] = 'Failed results-table-row'


            if self.test_case_result != self.failed:
                self.test_case_result = self.failed
                test_case_result_td = self.test_case_row.select('td')[2]
                test_case_result_td.string =  self.test_case_result
            # print(self.test_group_result)
            if self.test_group_result != self.failed:
                self.test_group_result = self.failed
                test_group_result_td = self.test_group_row.select('td')[2]
                test_group_result_td.string = self.test_group_result


    def test_comment(self,comment):
        self.log_div.append(comment)







