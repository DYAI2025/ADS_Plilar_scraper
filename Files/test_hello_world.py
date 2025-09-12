pytest.ini:
[pytest]
testpaths = Files
addopts = -v

test_hello_world.py:
def test_hello_world():
    assert 1 + 1 == 2