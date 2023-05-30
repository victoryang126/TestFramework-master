"""
pytest_configure(config)
当 pytest 开始执行时，会调用此钩子函数。你可以在这里进行一些全局的初始化设置，例如注册插件、加载配置文件等。

pytest_unconfigure(config)
当 pytest 执行完成后，会调用此钩子函数。你可以在这里进行一些清理操作，例如关闭数据库连接、释放资源等。

pytest_collection_modifyitems(config, items)
在测试用例收集完成后，会调用此钩子函数。你可以在这里修改收集到的测试用例的列表，例如对测试用例进行筛选、排序、重组等操作。

pytest_runtest_protocol(item, nextitem)
在每个测试用例运行之前和之后，会调用此钩子函数。你可以在这里实现自定义的测试用例运行逻辑，例如修改测试用例的输入、输出，执行特定的前置和后置操作等。

pytest_runtest_logreport(report)
每当测试用例执行完成后，会调用此钩子函数。你可以在这里处理测试结果，例如输出自定义的报告、记录日志等。

pytest_terminal_summary(terminalreporter, exitstatus, config)
在测试执行完成后，会调用此钩子函数。你可以在这里生成自定义的终端报告，例如统计测试结果、展示覆盖率报告等。

pytest_sessionstart(session)
当 pytest 开始整个测试会话时，会调用此钩子函数。你可以在这里进行一些全局的会话级别的初始化操作。

pytest_sessionfinish(session, exitstatus)
当 pytest 结束整个测试会话时，会调用此钩子函数。你可以在这里进行一些全局的会话级别的清理操作。
"""


"""
请帮我用pytest搭建一个测试框架，需要在报告的每个TestCase里面显示Timestamps TestSteps,Action Expect, Actual,Result,Timestamps 用函数获取当前的时间，具体到ms,TestSteps 在每个testcase 里面都是从数字1开始递增，这些元素要按照html table去显示


请帮我用pytest搭建一个测试框架，需要在报告的stdout result里面显示Timestamps TestSteps,Action ExpectResult, ActualResult,Result,Timestamps 用函数获取当前的时间，具体到ms,TestSteps 数字递增，这些元素要按照html table去显示

"""

"""
how to customize pytest html report
"""


"""
请帮我实现一个html,首先是一个title，然后title的左边是一个表格，TestInformaiton, 这个表格的header为User,PC,ARIA, 下面是另外一个表格TestSummary，header为 Pass,Fail,TBD,Total,Start,End,Duration, 最下面是Result的表格，header为Timestamp,TestCalss,File,Duration, Result，Result旁边有一个按钮，点击以后可以展开一个div，这个div在TestClassd一行里面在这个div 里面有另外一个表格，header为Timestamp,TestCase,File,Duration, Result，Result旁边有一个按钮，点击以后展开一个div, 这个div在testCase这个表格的一行里面这个里面是另外一个表格Timestamps TestSteps,Action Expect, Actual,Result
"""

"""
请帮我实现一个html,首先是一个title，然后title的左边是一个表格，TestInformaiton, 这个表格的header为User,PC,ARIA, 下面是另外一个表格TestSummary，header为 Pass,Fail,TBD,Total,Start,End,Duration, 最下面是Result的表格，header为Timestamp,TestClass,File,Duration, Result，Result下面的元素旁边有一个按钮，点击以后可以展开一个div，这个div作为Result表格的一行数据，默认是折叠起来的，当点击这个按钮以后，数据会展开，在这个div 里面有另外一个表格，名字叫做TestCases,header为Timestamp,TestCase,File,Duration, Result，Result下面的元素旁边有一个按钮，点击以后展开一个div,这个div作为TestCases的一行数据，默认是折叠起来的，当点击这个按钮以后，数据会展开这个里面是另外一个表格Timestamps TestSteps,Action Expect, Actual,Result"""
""""""