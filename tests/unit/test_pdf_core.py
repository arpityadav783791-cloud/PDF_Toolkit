from app.core.pdf.validator import PdfValidator
from app.core.pdf.reader import PdfReader
from app.core.pdf.merger import PdfMerger
def test_core(sample_pdf,tmp_path):
    assert PdfValidator().validate_file(sample_pdf)
    r=PdfReader(); r.open(sample_pdf); assert r.get_page_count()==1; r.close()
    out=tmp_path/'merged.pdf'; PdfMerger().merge([sample_pdf,sample_pdf],out)
    assert PdfValidator().check_page_count(out)==2
