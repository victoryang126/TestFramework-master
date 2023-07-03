
import copy
import traceback
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import datetime
import os
import getpass
import socket
import copy
import time
from nose.tools import assert_equal, assert_in
import logging
import pytest_html


class Report:

    def get_machine_name(self):
        return socket.gethostname()

    def get_user(self):
        return getpass.getuser()

    def __init__(self, template_file = "template.html" ):
        self.template_file = template_file
        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "")
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.template = self.env.get_template(self.template_file)
        self.data = {}

    def generate_html(self, results, output_file):
        # Extract file name and extension from output_file
        file_name = os.path.basename(output_file)
        file_name_without_ext = os.path.splitext(file_name)[0]

        # Add title and report_title attributes to data
        self.data['title'] = file_name_without_ext
        self.data['report_title'] = file_name

        # Get the current time and add it to the generated_date attribute in data
        now = datetime.datetime.now()
        self.data['generated_date'] = now.strftime('%d-%b-%Y at %H:%M:%S')
        self.data["machine"] = self.get_machine_name()
        self.data["user"] = self.get_user()
        self.data["results"] = results

        # Render the template and generate the HTML
        output = self.template.render(self.data)

        # Write the HTML to the file
        with open(output_file, 'w') as file:
            file.write(output)
        # absolute_path = os.path.abspath(output_file)
        file_link = f"<a href={os.path.abspath(output_file)}></a>"
        # file_link = f"file://{absolute_path}"
        html_report = Path(os.path.expandvars(output_file)).expanduser()
        print(f"generate customize html report: {html_report.absolute().as_uri()}")
        # print(f"generate customize html report: file:<a href={os.path.abspath(output_file)}></a>")




class Result:

    passed = "Passed"
    failed = "Failed"
    step = 0
    results = []
    def __init__(self):
       pass

    @classmethod
    def clear_results(cls):
        cls.results = []

    @classmethod
    def add_test_case(cls,test_case_name):
        test_case = {
            'duration': 0.0,
            'result': cls.failed, # default is Failed, if any exception happen, then the test calls will be failed
            'test_case': test_case_name,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            "test_groups":[]
        }
        cls.results.append(test_case)

    @classmethod
    def add_test_group(cls,test_group_name):
        cls.step = 0
        test_group = {
            'duration': 0.0,
            'result': cls.failed, # default is Failed, if any exception happen, then the test calls will be failed
            'test_group': test_group_name,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'test_steps':[]

        }
        #latest test class shall be -1
        cls.results[-1]["test_groups"].append(test_group)

    #TODO 根据ARIA 函数的名称和里面的参数去设置action，预期结果，世界结果
    @classmethod
    def test_step_aria(cls,aria_function_return,expect = None):

        # if len(aria_function_return) !=4:
        #Todo if the length is not equal 4. shall raise critical error in the stdout


        cls.step += 1

        if expect == None:
            result = aria_function_return[0]
            log = aria_function_return[1]
        else:
            #if the aria function have return value, then the index1 is the return result
            result,log = cls._compare_assert(aria_function_return[1], expect)
        test_step = {
            "test_step": f"Step {cls.step}",
            'action': aria_function_return[3],
            'expect': copy.deepcopy(expect),
            'actual': aria_function_return[1],
            'result': result,
            'log': log,
            'timestamp': aria_function_return[2]
        }
        # latest test class and test case
        cls.results[-1]["test_groups"][-1]["test_steps"].append(test_step)
    @classmethod
    def test_step2(cls, action, actual, expect,result):
        """

        :param action:
        :param expect:
        :param actual:
        :return:
        """
        cls.step +=1
        test_step = {
            "test_step":f"Step {cls.step}",
            'action': action,
            'expect': copy.deepcopy(expect),
            'actual': copy.deepcopy(actual),
            'result': result[0],
            'log':result[1],
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        #latest test class and test case
        cls.results[-1]["test_groups"][-1]["test_steps"].append(test_step)

    @classmethod
    def test_step(cls, action, actual, expect):
        """

        :param action:
        :param expect:
        :param actual:
        :return:
        """
        cls.step +=1
        result = cls._compare_assert(actual, expect)
        test_step = {
            "test_step":f"Step {cls.step}",
            'action': action,
            'expect': copy.deepcopy(expect),
            'actual': copy.deepcopy(actual),
            'result': result[0],
            'log':result[1],
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        #latest test class and test case
        cls.results[-1]["test_groups"][-1]["test_steps"].append(test_step)

    @classmethod
    def test_step_customize(cls,action, actual, expect,comparefunc):
        """

        :param action:
        :param expect:
        :param actual:
        :param comparefunc: compare function, the return value shall be two element array
        :return:
        """
        cls.step +=1
        result = comparefunc(expect, actual)
        # TODO, shall check if the function return a array with two element
        test_step = {
            "test_step":f"Step {cls.step}",
            'action': action,
            'expect': copy.deepcopy(expect),
            'actual': copy.deepcopy(actual),
            'result': result[0],
            'log':result[1],
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        #latest test class and test case
        cls.results[-1]["test_groups"][-1]["test_steps"].append(test_step)

    @classmethod
    def test_comment(cls,comment):
        test_step = {
            "test_step":"Comment",
            'action': comment,
            'expect': "",
            'actual': "actual",
            'result': "",
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        cls.results[-1]["test_groups"][-1]["test_steps"].append(test_step)

    @classmethod
    def _compare_assert(cls, actual,expect):
        try:
            # assert_equal(actual,expect)
            assert actual==expect
            return ('Passed',None)
        except AssertionError as e:
            #TODO the 2nd element shall be the details exception
            # return ('Failed',traceback.format_exc())
            return ('Failed',"Not Equal details")

    @classmethod
    def end_test_group(cls):
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        start_time = cls.results[-1]["test_groups"][-1]["timestamp"]
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        cls.results[-1]["test_groups"][-1]["duration"] =  "{:.4f}".format((end - start).total_seconds())
        test_steps =  cls.results[-1]["test_groups"][-1]["test_steps"]
        #get the test results in all test steps
        test_steps_results = [test_step["result"] for test_step in test_steps]
        if cls.failed not in test_steps_results:
            cls.results[-1]["test_groups"][-1]['result'] = cls.passed


    @classmethod
    def end_test_case(cls):
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        start_time = cls.results[-1]["timestamp"]
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        cls.results[-1]["duration"] =  "{:.4f}".format((end - start).total_seconds())
        test_groups =  cls.results[-1]["test_groups"]
        #get the test results in all test case
        test_groups_results = [test_group["result"] for test_group in test_groups]
        if cls.failed not in test_groups_results:
            cls.results[-1]['result'] = cls.passed

# class TestClass:
#
#     def __init__(self):



if __name__=="__main__":

    report = Report()
    # 使用示例


    Result.add_test_case('TestClassName')
    # 执行一些操作...
    Result.add_test_group('TestCase1')
    time.sleep(1)
    Result.test_step('Check if the array is equal,Check if the array is equal,Check if the array is equal,Check if the array is equal,Check if the array is equal', 'Expect1', 'Expect1')
    Result.test_step('Action2', 'Expect2', 'Expect2')

    Result.end_test_group()

    Expect1 = [i for i in range(100)]
    Actual1 = [i for i in range(100)]
    Actual1[1] = 10

    # raise Exception("Fail")
    # 执行一些操作...
    Result.add_test_group('TestCase2')
    time.sleep(0.5)
    Result.test_step('Check if the array is equal', Expect1, Actual1)
    Result.test_step('Action2', 'Expect2', 'Actual2')

    Result.end_test_group()

    Result.end_test_case()

    # Result.add_test_case('TestClassName2')
    # # 执行一些操作...
    # Result.add_test_group('TestCase3')
    # Result.test_step('Action1', 'Expect1', 'Expect1')
    # Result.test_step('Action2', 'Expect2', 'Expect2')
    # Result.test_step('Action3', 'Expect3', 'Expect3')
    # Result.end_test_group()
    #
    # # 执行一些操作...
    # Result.add_test_group('TestCase4')
    # Result.test_step('Action1', 'Expect1', 'Actual1')
    # Result.test_step('Action2', 'Expect2', 'Actual2')
    # Result.test_step('Action3', 'Expect3', 'Actual4')
    # Result.end_test_group()
    #
    # Result.end_test_case()

    report.generate_html(Result.results,"pytestReport.html")