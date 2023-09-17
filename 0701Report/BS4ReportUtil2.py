import sys
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
    def __init__(cls):
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


def bytearray_to_hex_list(byte_array):
    hex_list = ['0x{:02X}'.format(byte) for byte in byte_array]
    return hex_list

class HTMLReport:


    passed = "Passed"
    failed = "Failed"
    group = 0
    step = 0
    passed_groups = 0
    failed_groups = 0
    passed_steps = 0
    failed_steps = 0

    test_case_result = passed
    test_group_result = passed

    soup = BeautifulSoup(features="html.parser")
    html = soup.new_tag('html')
    soup.append(html)
    html_title = None
    report_path = ""

    # env_datas = {}
    # if html_title == None:
    #     frame_info = inspect.currentframe()
    #     # caller_frame = frame.f_back
    #     # co_filename = caller_frame.f_code.co_filename
    #     while frame_info.f_back is not None:
    #         frame_info = frame_info.f_back
    #         co_filename = frame_info.f_code.co_filename
    #     cls.html_title = os.path.basename(co_filename).split(".")[0]
    # else:
    #     cls.html_title = html_title
    #
    # cls.report_path = report_path

    # file_path = os.path.join(cls.report_path, f"{cls.html_title}.html")
    # cls.file = open(file_path, "w")
    # env_datas = _get_module_versions()
    #
    # cls._add_head_section() # Add the head section to the HTML report
    # cls._add_environment_section() # Add the environment section to the HTML report
    # cls._add_summary_section() # Add the summary section to the HTML report
    # cls._add_results_section() # Add the results section to the HTML report

    @classmethod
    def set_title(cls,html_title:str):
        cls.html_title = html_title


    @classmethod
    def set_report_path(cls,report_path):
        cls.report_path = report_path

    @classmethod
    def init(cls):
        if cls.html_title == None:
            frame_info = inspect.currentframe()
            # caller_frame = frame.f_back
            # co_filename = caller_frame.f_code.co_filename
            while frame_info.f_back is not None:
                frame_info = frame_info.f_back
                co_filename = frame_info.f_code.co_filename
            cls.html_title = os.path.basename(co_filename).split(".")[0]


        cls.env_datas = cls._get_module_versions()

        cls._add_head_section() # Add the head section to the HTML report
        cls._add_environment_section() # Add the environment section to the HTML report
        cls._add_summary_section() # Add the summary section to the HTML report
        cls._add_results_section() # Add the results section to the HTML report



    @classmethod
    def _get_machine_name(cls):
        return socket.gethostname() # Get the machine name

    @classmethod
    def _get_user(cls):
        return getpass.getuser() # Get the current user

    @classmethod
    def _get_module_versions(cls):
        #get the version of related module
        module_version = {}
        module_version["Python"] = sys.version
        module_version["BS4"] = bs4.__version__

        pass
        #TODO get version of related module
        return module_version

    @classmethod
    def add_env_datas(cls, env_datas:dict):
        """
        function used to update the module_versions,use to update the environment of html report
        :param env_datas:
        :return:
        """
        cls.env_datas.update(env_datas)

    @classmethod
    def _get_style_and_script(cls, html_file):
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

    @classmethod
    def _add_head_section(cls):
        # Add the head section to the HTML report
        head = cls.soup.new_tag('head')
        cls.html.append(head)

        meta = cls.soup.new_tag('meta', charset='utf-8')
        head.append(meta)

        title = cls.soup.new_tag('title')
        title.string = cls.html_title
        head.append(title)

        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "")
        template = os.path.join(template_path,"template.html")
        template_style,template_script = cls._get_style_and_script(template)

        style = cls.soup.new_tag('style')
        style.string = template_style
        head.append(style)

        cls.body = cls.soup.new_tag('body', onLoad='init()')
        cls.html.append(cls.body)

        script_tag = cls.soup.new_tag('script')
        script_tag.string = template_script
        cls.body.append(script_tag)

        h1 = cls.soup.new_tag('h1')
        h1.string = cls.html_title
        cls.body.append(h1)

        timestamp = cls.soup.new_tag('p')

        now = datetime.datetime.now()
        timestamp.string = f"Report Generate at {now.strftime('%Y-%m-%d %H:%M:%S')}"
        cls.body.append(timestamp)


    @classmethod
    def _add_environment_section(cls):
        # Add the environment section to the HTML report
        h2_env = cls.soup.new_tag('h2')
        h2_env.string = 'Environment'
        cls.body.append(h2_env)
        environment_data = {}
        environment_data["User"] = cls._get_user()
        environment_data["Machine"] = cls._get_machine_name()
        environment_data.update(cls.env_datas)
        env_table = cls.soup.new_tag('table', id='environment')
        cls.body.append(env_table)

        for key, value in environment_data.items():
            tr = cls.soup.new_tag('tr')
            env_table.append(tr)

            td1 = cls.soup.new_tag('td')
            td1.string = key
            tr.append(td1)

            td2 = cls.soup.new_tag('td')
            td2.string = value
            tr.append(td2)

    @classmethod
    def _add_summary_section(cls):
        # Add the summary section to the HTML report
        h2_summary_section = cls.soup.new_tag('h2')
        h2_summary_section.string = 'Summary'

        cls.body.append(h2_summary_section)

        summary_table = cls.soup.new_tag('table', id='testgroupsSummaryTable')
        cls.body.append(summary_table)

        headers = ['Category', 'Count', 'Show/Hide']
        header_row = cls.soup.new_tag('tr')
        summary_table.append(header_row)
        for header in headers:
            th = cls.soup.new_tag('th')
            th.string = header
            header_row.append(th)

        data = [
            ('Total test groups:', 'total', ''),
            ('Failed test groups:', 'Failed', 'Failed'),
            ('Passed test groups:', 'Passed', 'Passed')
        ]
        for item in data:
            category, count_id, checkbox_label = item
            tr = cls.soup.new_tag('tr')
            summary_table.append(tr)

            td1 = cls.soup.new_tag('td')
            td1.string = category
            tr.append(td1)

            td2 = cls.soup.new_tag('td', id=count_id)
            tr.append(td2)

            td3 = cls.soup.new_tag('td')
            tr.append(td3)

            if checkbox_label:
                checkbox = cls.soup.new_tag('input', type='checkbox', checked=True, onclick=f"toggletestgroupsRowVisibility('{checkbox_label}')")
                td3.append(checkbox)

    @classmethod
    def _add_results_section(cls):
        results_section = cls.soup.new_tag('h2')
        results_section.string = 'Results'
        cls.body.append(results_section)

        cls.results_table = cls.soup.new_tag('table', id='results-table')
        cls.body.append(cls.results_table)
        # results_section.insert_after(results_table)

        thead = cls.soup.new_tag('thead', id='results-table-head')
        cls.results_table.append(thead)

        headers = ['Timestamp', 'Test Case', 'Result', 'Duration(s)']
        header_row = cls.soup.new_tag('tr')
        thead.append(header_row)
        for header in headers:
            th = cls.soup.new_tag('th', col=header.lower().replace(' ', '-'))
            th.string = header
            header_row.append(th)

    @classmethod
    def add_test_case(cls, test_case):
        """
        Add a test case to the report.
        :param test_case_name: Name of the test case
        :return: None
        """
        if cls.group != 0:
            cls.end_test_case()
        cls.group = 0 # reinit the number
        cls.test_case = test_case
        cls.test_case_result = cls.passed
        cls.test_case_body = cls.soup.new_tag('tbody')
        cls.test_case_row = cls.soup.new_tag('tr',attrs={"class": "Passed results-table-row"})
        # Append the row to the results table
        cls.test_case_body.append(cls.test_case_row)
        cls.results_table.append(cls.test_case_body)

        cls.test_case_start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        result = cls.test_case_result
        duration = "0.0"
        # Create and append table cells for each column of data
        timestamp_cell = cls.soup.new_tag('td')
        timestamp_cell.string = cls.test_case_start_timestamp
        cls.test_case_row.append(timestamp_cell)

        test_case_cell = cls.soup.new_tag('td')
        test_case_cell.string = f"{cls.test_case}"
        cls.test_case_row.append(test_case_cell)

        result_cell = cls.soup.new_tag('td',attrs={"class": "col-data"})
        result_cell.string = result
        cls.test_case_row.append(result_cell)

        duration_cell = cls.soup.new_tag('td')
        duration_cell.string = duration
        cls.test_case_row.append(duration_cell)

        cls._add_extra_row_for_test_case()

        AriaLog.debug(f"start execute testcase{cls.test_case} at {cls.test_case_start_timestamp}")

    @classmethod
    def _add_extra_row_for_test_case(cls):
        # Add the additional row for test cases
        extra_row = cls.soup.new_tag('tr')
        cls.test_case_body.append(extra_row)

        extra_cell = cls.soup.new_tag('td', attrs = {"class":"extra","colspan":"5"})
        extra_row.append(extra_cell)

        div = cls.soup.new_tag('div')
        extra_cell.append(div)

        cls.test_group_table = cls.soup.new_tag('table', attrs = {"class":"test_groups"})
        div.append(cls.test_group_table)

        thead = cls.soup.new_tag('thead', attrs = {"class":"test_groups_header"})
        cls.test_group_table.append(thead)

        thead_row = cls.soup.new_tag('tr')
        thead.append(thead_row)

        headers = ['Timestamp', 'TestGroup',  'Result','Duration(s)']
        for header_text in headers:
            th = cls.soup.new_tag('th')
            th.string = header_text
            thead_row.append(th)


        # tbody = cls.soup.new_tag('tbody')

    @classmethod
    def add_test_group(cls, test_group:str)->None:
        """
        add group of test steps
        :param test_group: the name of the test group
        :return:
        """
        #handler the test group data for previous one
        if cls.group !=0:
            cls.end_test_group()

        cls.group += 1
        cls.step = 0
        cls.test_group_result = cls.passed
        cls.passed_steps = 0
        cls.failed_steps = 0
        # Create a new row for the test case in the test_cases_table
        cls.test_group_row = cls.soup.new_tag('tr',attrs={"class": "Passed results-table-row"})
        cls.test_group_table.append(cls.test_group_row)

        cls.test_group_start_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        duration = "0.0"
        result = cls.test_group_result

        # Create and append table cells for each column of data
        timestamp_cell = cls.soup.new_tag('td')
        timestamp_cell.string = cls.test_group_start_timestamp
        cls.test_group_row.append(timestamp_cell)

        cls.test_group = f"{cls.test_case}::{cls.group}::{test_group}"

        test_group_cell = cls.soup.new_tag('td')
        test_group_cell.string = cls.test_group
        cls.test_group_row.append(test_group_cell)


        result_cell = cls.soup.new_tag('td',attrs={"class": "col-data"})
        result_cell.string = result
        cls.test_group_row.append(result_cell)

        duration_cell = cls.soup.new_tag('td')
        duration_cell.string = str(duration)
        cls.test_group_row.append(duration_cell)

        cls._add_details_for_test_group()

        AriaLog.debug(f"start execute test group{cls.test_group} at {cls.test_group_start_timestamp}")

    @classmethod
    def _add_details_for_test_group(cls):

        # Add the details table with test steps
        details_row = cls.soup.new_tag('tr', attrs={"class": "details"})
        cls.test_group_table.append(details_row)

        details_cell = cls.soup.new_tag('td', colspan='6')
        details_row.append(details_cell)

        cls.test_steps_table = cls.soup.new_tag('table', attrs={"class": "test_steps"})
        details_cell.append(cls.test_steps_table)

        details_thead = cls.soup.new_tag('thead')
        cls.test_steps_table.append(details_thead)

        details_thead_row = cls.soup.new_tag('tr', attrs={"class": "test_step_header"})
        details_thead.append(details_thead_row)

        step_headers = ['Timestamps', 'TestSteps', 'Action', 'Expect', 'Actual', 'Result']
        th_classes = ["col-step-timestamps","col-step-teststeps","col-step-action","col-step-expect","col-step-actual","col-step-data"]
        for i,step_header in enumerate(step_headers):
            th = cls.soup.new_tag('th')
            th["class"] = th_classes[i]
            th.string = step_header
            details_thead_row.append(th)

    @classmethod
    def _end_test_case(cls):
        """
        this function used to get the duration and final data of test case
        :return:
        """
        cls.end_test_group()

        end_time = datetime.datetime.now()
        start_time = datetime.datetime.strptime(cls.test_case_start_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        test_case_duration =  "{:.4f}".format((end_time - start_time).total_seconds())
        test_case_duration_ele = cls.test_case_row.select('td')[3]
        test_case_duration_ele.string = test_case_duration
        if cls.failed_groups != 0:
            cls.test_case_row['class'] = 'Failed results-table-row'
            cls.test_case_result = cls.failed
            test_case_result_td = cls.test_case_row.select('td')[2]
            test_case_result_td.string =  cls.test_case_result

        if cls.test_case_result== cls.failed:
            AriaLog.critical(f"{cls.test_case} {cls.failed}")
        else:
            AriaLog.pass_log(f"{cls.test_case} {cls.passed}")

    @classmethod
    def end_test_group(cls):
        """
        this function is used to get the duration and final data of test group
        :return:
        """
        end_time = datetime.datetime.now()
        start_time = datetime.datetime.strptime(cls.test_group_start_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        test_group_duration =  "{:.4f}".format((end_time - start_time).total_seconds())
        test_group_duration_ele = cls.test_group_row.select('td')[3]
        test_group_duration_ele.string = test_group_duration
        if cls.failed_steps != 0:
            cls.failed_groups += 1
            cls.test_group_row['class'] = 'Failed results-table-row'
            cls.test_group_result = cls.failed
            test_group_result_td = cls.test_group_row.select('td')[2]
            test_group_result_td.string = cls.test_group_result
        else:
            cls.passed_groups += 1

        if cls.test_group_result== cls.failed:
            AriaLog.critical(f"{cls.test_group} {cls.failed}")
        else:
            AriaLog.pass_log(f"{cls.test_group} {cls.passed}")

    @classmethod
    def test_step_customize_result(cls, action:str, expect:Any, actual:Any, result:bool,log:str = ""):
        """
        function used to add customize step,the user can defined the data
        :param action: action
        :param expect:
        :param actual:
        :param result:
        :param log:
        :return:
        """
        cls.step +=1
        if result == True:
            attrs={"class": 'Passed'}
            cls.passed_steps +=1

        else:
            attrs={"class": 'Failed'}
            cls.failed_steps +=1
        # Create a new row for the test step in the test_steps_table
        test_step_row = cls.soup.new_tag('tr', attrs=attrs)
        cls.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data
        now = datetime.datetime.now()

        # cls.update_duration_result_for_testcase_testgroup(now,data)

        timestamp_cell = cls.soup.new_tag('td')
        timestamp_cell.string = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        test_step_row.append(timestamp_cell)

        test_step_cell = cls.soup.new_tag('td')
        test_step_cell.string = f"Step {cls.step}"
        test_step_row.append(test_step_cell)

        action_cell = cls.soup.new_tag('td')
        action_cell.append(str(action))
        test_step_row.append(action_cell)

        expect_cell = cls.soup.new_tag('td')
        expect_cell.append(str(expect))
        test_step_row.append(expect_cell)

        actual_cell = cls.soup.new_tag('td')
        actual_cell.append(str(actual))
        test_step_row.append(actual_cell)

        result_cell = cls.soup.new_tag('td',attrs={"class": "col-test-step-log"})
        result_cell.string = cls.passed if result else cls.failed
        test_step_row.append(result_cell)

        cls._add_test_log(log)
        # if use this kind method, there some problem with the report

    @classmethod
    def test_step_eq(cls, action:str, expect:Any, actual:Any):
        """
        function used to add customize step,the user can defined the data
        :param action: action
        :param expect:
        :param actual:
        :param data:
        :param log:
        :return:
        """
        result = actual == expect

        explanation = compare_eq_any_explanation(expect, actual)
        log = AriaLog.get_f_back_log(1, action, "\n".join(explanation))  # get the back_log


        cls.step +=1
        if result == True:
            attrs={"class": 'Passed'}
            cls.passed_steps +=1

        else:
            attrs={"class": 'Failed'}
            cls.failed_steps +=1
        # Create a new row for the test step in the test_steps_table
        test_step_row = cls.soup.new_tag('tr', attrs=attrs)
        cls.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data
        now = datetime.datetime.now()

        # cls.update_duration_result_for_testcase_testgroup(now,data)

        timestamp_cell = cls.soup.new_tag('td')
        timestamp_cell.string = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        test_step_row.append(timestamp_cell)

        test_step_cell = cls.soup.new_tag('td')
        test_step_cell.string = f"Step {cls.step}"
        test_step_row.append(test_step_cell)

        action_cell = cls.soup.new_tag('td')
        action_cell.append(str(action))
        test_step_row.append(action_cell)

        expect_cell = cls.soup.new_tag('td')
        expect_cell.append(str(expect))
        test_step_row.append(expect_cell)

        actual_cell = cls.soup.new_tag('td')
        actual_cell.append(str(actual))
        test_step_row.append(actual_cell)

        result_cell = cls.soup.new_tag('td',attrs={"class": "col-test-step-log"})
        result_cell.string = cls.passed if result else cls.failed
        test_step_row.append(result_cell)

        cls._add_test_log(log)
        # if use this kind method, there some problem with the report

    @classmethod
    def test_step_aria(cls, aria_function_return,expect = None):

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
            #compare the data
            result = actual == expect

            explanation = compare_eq_any_explanation(expect,actual)
            log = AriaLog.get_deep_f_back_log(action,"\n".join(explanation)) #get the back_log

        cls.step +=1
        if result == True:
            attrs={"class": 'Passed'}
            cls.passed_steps +=1
        else:
            attrs={"class": 'Failed'}
            cls.failed_steps +=1
        # Create a new row for the test step in the test_steps_table
        test_step_row = cls.soup.new_tag('tr', attrs=attrs)
        cls.test_steps_table.append(test_step_row)

        # Create and append table cells for each column of data


        # cls.update_duration_result_for_testcase_testgroup(now,data)

        timestamp_cell = cls.soup.new_tag('td')
        timestamp_cell.string = timestamp
        test_step_row.append(timestamp_cell)

        test_step_cell = cls.soup.new_tag('td')
        test_step_cell.string = f"Step {cls.step}"
        test_step_row.append(test_step_cell)

        action_cell = cls.soup.new_tag('td')
        action_cell.append(str(action))
        test_step_row.append(action_cell)

        expect_cell = cls.soup.new_tag('td')
        expect_cell.append(str(expect))
        test_step_row.append(expect_cell)

        actual_cell = cls.soup.new_tag('td')
        actual_cell.append(str(actual))
        test_step_row.append(actual_cell)

        result_cell = cls.soup.new_tag('td',attrs={"class": "col-test-step-log"})
        result_cell.string = cls.passed if result else cls.failed
        test_step_row.append(result_cell)

        if result == False:
            cls._add_test_log(log)
        else:
            cls._add_test_log()
        # if use this kind method, there some problem with the report




    @classmethod
    def _add_test_log(cls,log = ""):
        log_row = cls.soup.new_tag('tr')
        td_colspan = cls.soup.new_tag('td',attrs = {"colspan": "6"})
        cls.log_div = cls.soup.new_tag('div',attrs = {"class": "log"})
        # cls.log_div.string = ""
        cls.log_div.append(f"{log}\n")
        td_colspan.append(cls.log_div)
        log_row.append(td_colspan)
        cls.test_steps_table.append(log_row)



    @classmethod
    def test_comment(cls,comment):
        cls.log_div.append(f"{comment}\n")

    @classmethod
    def generate_report(cls):

        cls._end_test_case()

        file_path = os.path.join(cls.report_path, f"{cls.html_title}.html")
        with open(file_path, "w") as file:
        # cls.file.write(cls.soup.prettify(formatter=custom_formatter))
            file.write(str(cls.html))
            file_path = os.path.join(cls.report_path,f"{cls.html_title}.html")
            html_report = Path(os.path.expandvars(file_path)).expanduser()
            print(f"generate customize html report: {html_report.absolute().as_uri()}")



