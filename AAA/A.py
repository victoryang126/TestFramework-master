import re

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# the metaclass will automatically get passed the same arguments that we pass to `type`
def camel_to_snake_case(name, bases, attrs):
    """Return a class object, with its attributes from camelCase to snake_case."""
    print("Calling the metaclass camel_to_snake_case to construct class: {}".format(name))

    # pick up any attribute that doesn't start with '__' and snakecase it
    snake_attrs = {}
    for attr_name, attr_val in attrs.items():
        if not attr_name.startswith('__'):
            snake_attrs[convert(attr_name)] = attr_val
        else:
            snake_attrs[attr_name] = attr_val
    return type(name, bases, snake_attrs) # let `type` do the class creation

class MyVector(metaclass=camel_to_snake_case):
    def addToVector(self): pass
    def subtractFromVector(self, other): pass
    def calculateDotProduct(self, other): pass
    def calculateCrossProduct(self, other): pass
    def calculateTripleProduct(self, other): pass

print([a for a in dir(MyVector) if not a.startswith('__')])