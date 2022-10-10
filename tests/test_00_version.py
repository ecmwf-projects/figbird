import bluejay


def test_version() -> None:
    assert bluejay.__version__ != "999"
