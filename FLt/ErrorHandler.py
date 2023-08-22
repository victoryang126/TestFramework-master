import traceback
def divide_numbers(a, b):
    # result = a / b
    # try:
        result = a / b
    #     print("result：", result)
    # except Exception:
    #     traceback.print_exc()

divide_numbers(10, 2)
divide_numbers(10, 0)
divide_numbers(10, '2')
divide_numbers(10, [])   #  unsupported operand type(s) for /: 'int' and 'list'

#     print("ZeroDivisionError！")
#     print(traceback.format_exc())
# except TypeError:
#     print("TypeError！")
#     print(traceback.format_exc())
# except Exception as e:
#     print("Unknow error：", str(e))
#     print(traceback.format_exc())
