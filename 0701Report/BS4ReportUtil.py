from pathlib import Path
import bs4
from bs4 import BeautifulSoup
import getpass
import socket
import os
import datetime

from typing import Any
import inspect
from CompareUtil import *





class AriaLog:

    DEBUG = 3
    INFO = 2
    WARNING = 1
    CRITICAL = 0
    LEVEL = 0
    #the Critical info shall output
    def __init__(self):
        pass

    @classmethod
    def set_log_level(cls,level):
        cls.LEVEL = level

    @classmethod
    def get_deep_f_back_log(cls,message = "",explanation=""):
        frame_info = inspect.currentframe().f_back
        code_infos = []
        while frame_info.f_back is not None:
            frame_info = frame_info.f_back
            line_number = frame_info.f_lineno
            file_name = frame_info.f_code.co_filename
            func_name = inspect.getframeinfo(frame_info).function
            code_infos.append(f"called at line {line_number} in function {func_name} file {file_name}")
            # code_info = f"called at line {line_number} in file {file_name}\n"
        code_info = "\n".join(code_infos)
        return f" {message}\n:{code_info} Details Failure Info \n{explanation}"

    @classmethod
    def get_f_back_log(cls,f_back_no:int = 0,message:Any = "",explanation = ""):
        frame_info = inspect.currentframe().f_back
        #TODO shall consider to set  limit of f_back_no
        f_back_no_type = type(f_back_no)
        if f_back_no_type != int :
            cls.critical(f"TestLog::get_f_back_log::arg::f_back_no shall be int but not {f_back_no_type}")
            #TODO shall we need raise exception ?
        else:
            while f_back_no != 0:
                frame_info = frame_info.f_back
                f_back_no -= 1
        line_number = frame_info.f_lineno
        file_name = frame_info.f_code.co_filename
        return f" {message}\n:called at line {line_number} in file {file_name} \nDetails Failure Info \n{explanation}"

    @classmethod
    def info(cls,comment:Any):
        if cls.LEVEL >=2:
            print(comment)

    @classmethod
    def debug(cls,comment:Any):
        if cls.LEVEL >= 3:
            print(f'\033[30;1m{comment}\033[0m')

    @classmethod
    def critical(cls, comment:Any):
        print(f'\033[31;1m{comment}\033[0m')

    @classmethod
    def warning(cls,comment:Any):
        print(f'\033[33;1m{comment}\033[0m')

    @classmethod
    def pass_log(cls,comment:Any):
        print(f'\033[32;1m{comment}\033[0m')


def custom_formatter(tag):
    if tag.string:
        tag.string = tag.string.strip()
        return tag

class HTMLReport:

    passed = "Passed"
    failed = "Failed"
    group = 0
    step = 0
    passed_groups = 0
    failed_groups = 0
    passed_steps = 0
    failed_steps = 0

    def __init__(self,html_title=None,report_path=""):

        self.test_case_result = self.passed
        self.test_group_result = self.passed

        self.soup = BeautifulSoup(features="html.parser")
        self.html = self.soup.new_tag('html')
        self.soup.append(self.html)

        if html_title == None:
            frame_info = inspect.currentframe()
            # caller_frame = frame.f_back
            # co_filename = caller_frame.f_code.co_filename
            while frame_info.f_back is not None:
                frame_info = frame_info.f_back
                co_filename = frame_info.f_code.co_filename
            self.html_title = os.path.basename(co_filename).split(".")[0]
        else:
            self.html_title = html_title

        self.report_path = report_path

        file_path = os.path.join(self.report_path, f"{self.html_title}.html")
        self.file = open(file_path, "w")
        self.env_datas = self._get_module_versions()

        self._add_head_section() # Add the head section to the HTML report
        self._add_environment_section() # Add the environment section to the HTML report
        self._add_summary_section() # Add the summary section to the HTML report
        self._add_results_section() # Add the results section to the HTML report




    def _get_machine_name(self):
        return socket.gethostname() # Get the machine name

    def _get_user(self):
        return getpass.getuser() # Get the current user


    def _get_module_versions(self):
        #get the version of related module
        module_version = {}
        module_version["BS4"] = bs4.__version__
        pass
        #TODO get version of related module
        return module_version


    def add_env_datas(self, env_datas:dict):
        """
        function used to update the module_versions,use to update the environment of html report
        :param env_datas:
        :return:
        """
        self.env_datas.update(env_datas)

    def _get_style_and_script(self, html_file):
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

    def _add_head_section(self):
        # Add the head section to the HTML report
        head = self.soup.new_tag('head')
        self.html.append(head)

        meta = self.soup.new_tag('meta', charset='utf-8')
        head.append(meta)

        title = self.soup.new_tag('title')
        title.string = self.html_title
        head.append(title)

        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "")
        template = os.path.join(template_path,"template.html")
        template_style,template_script = self._get_style_and_script(template)

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



    def _add_environment_section(self):
        # Add the environment section to the HTML report
        h2_env = self.soup.new_tag('h2')
        h2_env.string = 'Environment'
        self.body.append(h2_env)
        environment_data = {}
        environment_data["User"] = self._get_user()
        environment_data["Machine"] = self._get_machine_name()
        environment_data.update(self.env_datas)
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

    def _add_summary_section(self):
        # Add the summary section to the HTML report
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

    def _add_results_section(self):
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


    def add_test_case(self, test_case):
        """
        Add a test case to the report.
        :param test_case_name: Name of the test case
        :return: None
        """
        if self.group != 0:
            self.end_test_case()
        self.group = 0 # reinit the number
        self.test_case = test_case
        self.test_case_result = self.passed
        self.test_case_body = self.soup.new_tag('tbody')
        self.test_case_row = self.soup.new_tag('tr',attrs={"class": "Passed results-table-row"})
        # Append the row to the results table
        self.test_case_body.append(self.test_case_row)
        self.results_table.append(self.test_case_body)

        self.test_case_start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        result = self.test_case_result
        duration = "0.0"
        # Create and append table cells for each column of data
        timestamp_cell = self.soup.new_tag('td')
        timestamp_cell.string = self.test_case_start_timestamp
        self.test_case_row.append(timestamp_cell)

        test_case_cell = self.soup.new_tag('td')
        test_case_cell.string = f"{self.html_title}::{self.test_case}"
        self.test_case_row.append(test_case_cell)

        result_cell = self.soup.new_tag('td',attrs={"class": "col-result"})
        result_cell.string = result
        self.test_case_row.append(result_cell)

        duration_cell = self.soup.new_tag('td')
        duration_cell.string = duration
        self.test_case_row.append(duration_cell)

        self._add_extra_row_for_test_case()

        AriaLog.debug(f"start execute testcase{self.test_case} at {self.test_case_start_timestamp}")


    def _add_extra_row_for_test_case(self):
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


    def add_test_group(self, test_group:str)->None:
        """
        add group of test steps
        :param test_group: the name of the test group
        :return:
        """
        #handler the test group result for previous one
        if self.group !=0:
            self.end_test_group()

        self.group += 1
        self.step = 0
        self.test_group_result = self.passed
        self.passed_steps = 0
        self.failed_steps = 0
        # Create a new row for the test case in the test_cases_table
        self.test_group_row = self.soup.new_tag('tr',attrs={"class": "Passed results-table-row"})
        self.test_group_table.append(self.test_group_row)

        self.test_group_start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        duration = "0.0"
        result = self.test_group_result

        # Create and append table cells for each column of data
        timestamp_cell = self.soup.new_tag('td')
        timestamp_cell.string = self.test_group_start_timestamp
        self.test_group_row.append(timestamp_cell)

        self.test_group = f"{self.html_title}::{self.test_case}::{self.group}::{test_group}"

        test_group_cell = self.soup.new_tag('td')
        test_group_cell.string = self.test_group
        self.test_group_row.append(test_group_cell)


        result_cell = self.soup.new_tag('td',attrs={"class": "col-result"})
        result_cell.string = result
        self.test_group_row.append(result_cell)

        duration_cell = self.soup.new_tag('td')
        duration_cell.string = str(duration)
        self.test_group_row.append(duration_cell)

        self._add_details_for_test_group()

        AriaLog.debug(f"start execute test group{self.test_group} at {self.test_group_start_timestamp}")


    def _add_details_for_test_group(self):

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
        th_classes = ["col-step-timestamps","col-step-teststeps","col-step-action","col-step-expect","col-step-actual","col-step-result"]
        for i,step_header in enumerate(step_headers):
            th = self.soup.new_tag('th')
            th["class"] = th_classes[i]
            th.string = step_header
            details_thead_row.append(th)

    def _end_test_case(self):
        """
        this function used to get the duration and final result of test case
        :return:
        """
        self.end_test_group()

        end_time = datetime.datetime.now()
        start_time = datetime.datetime.strptime(self.test_case_start_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        test_case_duration =  "{:.4f}".format((end_time - start_time).total_seconds())
        test_case_duration_ele = self.test_case_row.select('td')[3]
        test_case_duration_ele.string = test_case_duration
        if self.failed_groups != 0:
            self.test_case_row['class'] = 'Failed results-table-row'
            self.test_case_result = self.failed
            test_case_result_td = self.test_case_row.select('td')[2]
            test_case_result_td.string =  self.test_case_result

        if self.test_case_result== self.failed:
            AriaLog.critical(f"HTMLReport::{self.test_case} {self.failed}")
        else:
            AriaLog.pass_log(f"HTMLReport::{self.test_case} {self.passed}")

    def end_test_group(self):
        """
        this function is used to get the duration and final result of test group
        :return:
        """
        end_time = datetime.datetime.now()
        start_time = datetime.datetime.strptime(self.test_group_start_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        test_group_duration =  "{:.4f}".format((end_time - start_time).total_seconds())
        test_group_duration_ele = self.test_group_row.select('td')[3]
        test_group_duration_ele.string = test_group_duration
        if self.failed_steps != 0:
            self.failed_groups += 1
            self.test_group_row['class'] = 'Failed results-table-row'
            self.test_group_result = self.failed
            test_group_result_td = self.test_group_row.select('td')[2]
            test_group_result_td.string = self.test_group_result
        else:
            self.passed_groups += 1

        if self.test_group_result== self.failed:
            AriaLog.critical(f"HTMLReport::{self.test_group} {self.failed}")
        else:
            AriaLog.pass_log(f"HTMLReport::{self.test_group} {self.passed}")


    def test_step_customize_result(self, action:str, expect:Any, actual:Any, result:bool,log:str = ""):
        """
        function used to add customize step,the user can defined the result
        :param action: action
        :param expect:
        :param actual:
        :param result:
        :param log:
        :return:
        """
        self.step +=1
        if result == True:
            attrs={"class": 'Passed'}
            self.passed_steps +=1

        else:
            attrs={"class": 'Failed'}
            self.failed_steps +=1
        # Create a new row for the test step in the test_steps_table
        test_step_row = self.soup.new_tag('tr', attrs=attrs)
        self.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data
        now = datetime.datetime.now()

        # self.update_duration_result_for_testcase_testgroup(now,result)

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
        result_cell.string = self.passed if result else self.failed
        test_step_row.append(result_cell)

        self._add_test_log(log)
          # if use this kind method, there some problem with the report


    def test_step_eq(self, action:str, expect:Any, actual:Any):
        """
        function used to add customize step,the user can defined the result
        :param action: action
        :param expect:
        :param actual:
        :param result:
        :param log:
        :return:
        """
        result = actual == expect

        explanation = compare_eq_any_explanation(expect, actual)
        log = AriaLog.get_f_back_log(1, action, "\n".join(explanation))  # get the back_log


        self.step +=1
        if result == True:
            attrs={"class": 'Passed'}
            self.passed_steps +=1

        else:
            attrs={"class": 'Failed'}
            self.failed_steps +=1
        # Create a new row for the test step in the test_steps_table
        test_step_row = self.soup.new_tag('tr', attrs=attrs)
        self.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data
        now = datetime.datetime.now()

        # self.update_duration_result_for_testcase_testgroup(now,result)

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
        result_cell.string = self.passed if result else self.failed
        test_step_row.append(result_cell)

        self._add_test_log(log)
          # if use this kind method, there some problem with the report


    def test_step_aria(self, aria_function_return,expect = None):

        if len(aria_function_return) !=4 and isinstance(aria_function_return,List):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            action = aria_function_return
            expect = None
            actual = "call execute arai function fail"
            result = False
            log = AriaLog.get_deep_f_back_log(f"the return value of aria function shall be a list with 4 element")
        elif expect == None:
            result,actual,timestamp,action = aria_function_return[0],aria_function_return[1],aria_function_return[2],aria_function_return[3]
            log = AriaLog.get_deep_f_back_log(action) #get the back_log
        else:
            result, actual, timestamp, action = aria_function_return[0], aria_function_return[1], aria_function_return[
                2], aria_function_return[3],
            #compare the result
            result = actual == expect

            explanation = compare_eq_any_explanation(expect,actual)
            log = AriaLog.get_deep_f_back_log(action,"\n".join(explanation)) #get the back_log

        self.step +=1
        if result == True:
            attrs={"class": 'Passed'}
            self.passed_steps +=1
        else:
            attrs={"class": 'Failed'}
            self.failed_steps +=1
        # Create a new row for the test step in the test_steps_table
        test_step_row = self.soup.new_tag('tr', attrs=attrs)
        self.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data


        # self.update_duration_result_for_testcase_testgroup(now,result)

        timestamp_cell = self.soup.new_tag('td')
        timestamp_cell.string = timestamp
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
        result_cell.string = self.passed if result else self.failed
        test_step_row.append(result_cell)

        if result == False:
            self._add_test_log(log)
        else:
            self._add_test_log()
          # if use this kind method, there some problem with the report

    def update_report(self):
        self.file.write(self.soup.prettify(formatter='html5'))

    def _add_test_log(self,log = ""):
        log_row = self.soup.new_tag('tr')
        td_colspan = self.soup.new_tag('td',attrs = {"colspan": "6"})
        self.log_div = self.soup.new_tag('div',attrs = {"class": "log"})
        # self.log_div.string = ""
        self.log_div.append(f"{log}\n")
        td_colspan.append(self.log_div)
        log_row.append(td_colspan)
        self.test_steps_table.append(log_row)




    def test_comment(self,comment):
        self.log_div.append(f"{comment}\n")


    def generate_report(self):

        self._end_test_case()
        # self.file.write(self.soup.prettify(formatter=custom_formatter))
        self.file.write(str(self.html))
        file_path = os.path.join(self.report_path,f"{self.html_title}.html")
        html_report = Path(os.path.expandvars(file_path)).expanduser()
        print(f"generate customize html report: {html_report.absolute().as_uri()}")
        self.file.close()


