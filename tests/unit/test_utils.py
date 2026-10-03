from app.utils.pdf_utils import parse_page_ranges

def test_ranges():
    assert parse_page_ranges("1-3,5", 6) == [0, 1, 2, 4]
