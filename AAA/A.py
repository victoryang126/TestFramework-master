
def add(x,y):
    print(f"{x} + {y} = {x+y}")

def test():
    print("test")

def execute(test_func,case_name,*args,**kwargs):
    test_func(*args,**kwargs)

execute(add,2,3,4)
execute(test,2)
