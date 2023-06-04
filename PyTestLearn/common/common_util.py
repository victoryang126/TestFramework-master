class CommonUtil:
    def setup_class(self):
        print("execute before each class")

    def teardown_class(self):
        print("execute after each class")

    def setup_method(self):
        print("execute before each test case")

    def teardown_method(self):
        print("execute after each test case")
