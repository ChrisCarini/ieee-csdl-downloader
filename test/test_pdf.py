from pathlib import Path
from typing import List

import pikepdf

from ieee_csdl_downloader.pdf import sorted_nicely


def test_sorted_nicely() -> None:
    # given
    files = [
        'j3188.pdf',
        'j3032.pdf',
        'j3001ad.pdf',
        'j3toc.pdf',
        'j3c1.pdf',
    ]

    # when
    result = sorted_nicely(files)

    # then
    assert result == [
        'j3c1.pdf',
        'j3toc.pdf',
        'j3001ad.pdf',
        'j3032.pdf',
        'j3188.pdf',
    ]


def merge_pdf(sorted_files: List[str], merged_pdf_name: Path) -> None:
    pdf = pikepdf.Pdf.new()

    # loop through all PDFs
    for filename in sorted_files:
        # rb for read binary
        src = pikepdf.Pdf.open(filename)

        # #TODO(ChrisCarini) - Was trying to get any annotation links to files and re-map them to the respective page.
        # # TL;DR; it's non-trivial, and I spend ~1hr+ to figure it out and had no luck. Moving on for now since
        # # this is detracting from the original goal (scrape publications & combine multi-pdf ZIP files).
        # urls = []
        # for page in src.pages:
        #     if page.get("/Annots") is None:
        #         continue
        #     for annots in page.get("/Annots"):
        #         a = annots.get("/A")
        #         file_link = a.get('/F').get('/F')
        #         if str(file_link).endswith('.pdf'):
        #             link_to_page = str(file_link).split('.pdf')[0][3:]
        #
        #         new_link = pikepdf.Dictionary({
        #             "/A": {
        #                 "/URI": f"#page={link_to_page}",
        #             },
        #             "/Border": annots.get('/Border'),
        #             "/H": annots.get('/H'),
        #             "/Rect": annots.get('/Rect'),
        #             "/Subtype": annots.get('/Subtype'),
        #             "/Type": annots.get('/Type'),
        #         })
        #         page.Annots = pdf.make_indirect(pikepdf.Array([new_link]))
        #         # uri = a.get("/URI")
        #         # if uri is not None:
        #         #     print("[+] URL Found:", uri)
        #         #     urls.append(uri)

        pdf.pages.extend(src.pages)

    pdf.remove_unreferenced_resources()

    pdf.save(merged_pdf_name)
