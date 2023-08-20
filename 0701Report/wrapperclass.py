class A:
    @staticmethod
    def method1():
        return "Result from method1"

    @staticmethod
    def method2():
        return "Result from method2"

class B(A):
    @staticmethod
    def method3():
        return "Result from method3"

# Define the decorator
def process_return_values(cls):
    class WrappedClass(cls):
        @staticmethod
        def process_result(success, result):
            return success, result

        @classmethod
        def execute_method(cls, method_name, *args, **kwargs):
            try:
                result = getattr(super(), method_name)(*args, **kwargs)
                return cls.process_result(True, result)
            except Exception as e:
                return cls.process_result(False, str(e))

        def __getattribute__(self, name):
            attr = super().__getattribute__(name)
            if callable(attr):
                return lambda *args, **kwargs: self.execute_method(name, *args, **kwargs)
            return attr

    return WrappedClass

# Decorate class B
@process_return_values
class DecoratedB(B):
    pass

# Test the decorated class
success1, result1 = DecoratedB.method1()
print(success1, result1)  # Output: True, 'Result from method1'

success2, result2 = DecoratedB.method2()
print(success2, result2)  # Output: True, 'Result from method2'

success3, result3 = DecoratedB.method3()
print(success3, result3)  # Output: True, 'Result from method3'

success4, result4 = DecoratedB.non_existent_method()
print(success4, result4)  # Output: False, "'DecoratedB' object has no attribute 'non_existent_method'"
