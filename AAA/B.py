from A import step
import pytest
import traceback

def test_call_test_step():
    step()

def test_call_test_step2():
    try:
        assert [1,2]==[1,1,3]
    except AssertionError as e:
        print(traceback.format_exc())

if __name__ == "__main__":
    pytest.main(['-v','B.py'  ,'--html=test.html','--self-contained-html'])