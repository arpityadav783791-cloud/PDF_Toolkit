from app.core.pdf.splitter import PdfSplitter

def test_split(sample_pdf, tmp_path):
    outputs = PdfSplitter().split_every_page(sample_pdf, tmp_path)
    assert len(outputs) == 1
