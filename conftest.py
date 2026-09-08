import pytest

@pytest.fixture
def collector(self):
    return BooksCollector()