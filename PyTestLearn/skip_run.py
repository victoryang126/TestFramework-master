import pytest

if __name__ == "__main__":
    # pass
    pytest.main(['-sv', './testcase/py_test.py', '--html=./report/skip.html', '--self-contained-html'])