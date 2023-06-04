
import copy
from jinja2 import Environment, FileSystemLoader
import datetime
import os
import getpass
import socket
import copy

class Report:

    def get_machine_name(self):
        return socket.gethostname()

    def get_user(self):
        return getpass.getuser()

    def __init__(self, template_file = "template.html" ):
        self.template_file = template_file
        self.env = Environment(loader=FileSystemLoader('.'))
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
        # file_link = f"file://{absolute_path}"
        print(f"generate customize html report: file://{os.path.abspath(output_file)}")




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
    def add_test_class(cls,test_class_name):
        test_class = {
            'duration': 0.0,
            'result': cls.failed, # default is Failed, if any exception happen, then the test calls will be failed
            'test_class': test_class_name,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            "test_cases":[]
        }
        cls.results.append(test_class)

    @classmethod
    def add_test_case(cls,test_case_name):
        cls.step = 0
        test_case = {
            'duration': 0.0,
            'result': cls.failed, # default is Failed, if any exception happen, then the test calls will be failed
            'test_case': test_case_name,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'test_steps':[]

        }
        #latest test class shall be -1
        cls.results[-1]["test_cases"].append(test_case)

    @classmethod
    def test_step(cls, action, expect, actual):
        """

        :param action:
        :param expect:
        :param actual:
        :return:
        """
        cls.step +=1
        result = cls._compare_assert(expect, actual)
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
        cls.results[-1]["test_cases"][-1]["test_steps"].append(test_step)

    @classmethod
    def test_step_customize(cls,action,expect,actual,comparefunc):
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
        cls.results[-1]["test_cases"][-1]["test_steps"].append(test_step)

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
        cls.results[-1]["test_cases"][-1]["test_steps"].append(test_step)

    @classmethod
    def _compare_assert(cls, expect, actual):
        try:
            assert expect == actual
            return ('Passed',None)
        except AssertionError as e:
            #TODO the 2nd element shall be the details exception
            return ('Failed',"lllll")

    @classmethod
    def end_test_case(cls):
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        start_time = cls.results[-1]["test_cases"][-1]["timestamp"]
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        cls.results[-1]["test_cases"][-1]["duration"] =  "{:.4f}".format((end - start).total_seconds())
        test_steps =  cls.results[-1]["test_cases"][-1]["test_steps"]
        #get the test results in all test steps
        test_steps_results = [test_step["result"] for test_step in test_steps]
        if cls.failed not in test_steps_results:
            cls.results[-1]["test_cases"][-1]['result'] = cls.passed


    @classmethod
    def end_test_class(cls):
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        start_time = cls.results[-1]["timestamp"]
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        cls.results[-1]["duration"] =  "{:.4f}".format((end - start).total_seconds())
        test_cases =  cls.results[-1]["test_cases"]
        #get the test results in all test case
        test_cases_results = [test_case["result"] for test_case in test_cases]
        if cls.failed not in test_cases_results:
            cls.results[-1]['result'] = cls.passed

# class TestClass:
#
#     def __init__(self):



if __name__=="__main__":

    report = Report()
    # 使用示例


    Result.add_test_class('TestClassName')
    # 执行一些操作...
    Result.add_test_case('TestCase1')
    Result.test_step('Check if the array is equal,Check if the array is equal,Check if the array is equal,Check if the array is equal,Check if the array is equal', 'Expect1', 'Expect1')
    Result.test_step('Action2', 'Expect2', 'Expect2')
    Result.test_step('Action3', 'Expect3', 'Expect3')
    Result.end_test_case()

    Expect1 = [i for i in range(100)]
    Actual1 = [i for i in range(100)]
    Actual1[1] = 10
    # 执行一些操作...
    Result.add_test_case('TestCase2')
    Result.test_step('Check if the array is equal,Check if the array is equal,Check if the array is equal,Check if the array is equal,Check if the array is equal', Expect1, Actual1)
    Result.test_step('Action2', 'Expect2', 'Actual2')
    Result.test_step('Action3', 'Expect3', 'Actual4')
    Result.end_test_case()

    Result.end_test_class()

    Result.add_test_class('TestClassName2')
    # 执行一些操作...
    Result.add_test_case('TestCase3')
    Result.test_step('Action1', 'Expect1', 'Expect1')
    Result.test_step('Action2', 'Expect2', 'Expect2')
    Result.test_step('Action3', 'Expect3', 'Expect3')
    Result.end_test_case()

    # 执行一些操作...
    Result.add_test_case('TestCase4')
    Result.test_step('Action1', 'Expect1', 'Actual1')
    Result.test_step('Action2', 'Expect2', 'Actual2')
    Result.test_step('Action3', 'Expect3', 'Actual4')
    Result.end_test_case()

    Result.end_test_class()

    report.generate_html(Result.results,"pytestReport.html")