import re
import shutil
import tempfile
import zipfile

from pathlib import Path
from typing import List

import pikepdf

from ieee_csdl_downloader.config import get_download_dir


def unzip_and_merge(output_pdf_file: Path, zip_file: Path):  # pragma: nocover
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # create temp dir
        with tempfile.TemporaryDirectory(dir=get_download_dir()) as temp_dirpath:
            # extract files
            zip_ref.extractall(temp_dirpath)

            # If just TOC file, rename
            pdf_filenames = [p.name for p in list(Path(temp_dirpath).glob('*.pdf'))]
            if 'toc.pdf' in pdf_filenames:
                prefix = set()
                for f in pdf_filenames:
                    prefix.add(f.split('/')[-1][:3])

                prefix = prefix - {'toc'}

                shutil.move(
                    src=Path(temp_dirpath) / 'toc.pdf',  # type: ignore
                    dst=Path(temp_dirpath) / f'{prefix.pop()}toc.pdf',
                )

            sorted_files = sorted_nicely([str(x) for x in list(Path(temp_dirpath).glob('*.pdf'))])

            merge_pdf(sorted_files, output_pdf_file)


def sorted_nicely(files: List[str]) -> List[str]:
    """Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text  # noqa: E731
    alphanum_key = lambda key: [convert(c) for c in re.split(r'(\d+)', key)]  # noqa: E731
    return sorted(files, key=alphanum_key)


def merge_pdf(sorted_files: List[str], merged_pdf_name: Path) -> None:  # pragma: nocover
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
