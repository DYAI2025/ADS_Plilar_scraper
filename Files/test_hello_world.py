"""Sanity check tests for pytest configuration."""


def test_pytest_is_configured():
    """Ensure pytest configuration file is picked up correctly."""
    assert True


def test_basic_math():
    """A minimal smoke test to ensure pytest executes."""
    assert 1 + 1 == 2
