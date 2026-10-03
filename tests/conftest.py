import pytest, pymupdf
@pytest.fixture
def sample_pdf(tmp_path):
    p=tmp_path/'sample.pdf'; d=pymupdf.open() if False else pymupdf.open()
    page=d.new_page(); page.insert_text((72,72),'PDF Toolkit Test'); d.save(p); d.close(); return p
