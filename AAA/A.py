import traceback
def step():
    try:
        assert [1,2]==[1,1]
    except AssertionError as e:
        print("Assertion failed:", str(e))
        traceback.print_exc()
        # print(traceback.format_exc())

