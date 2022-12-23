import shutil

from datetime import datetime
from pathlib import Path
from typing import List, Optional

import requests

from ieee_csdl_downloader.auth import COOKIES
from ieee_csdl_downloader.constants import DOWNLOAD_DIR, DOWNLOAD_START_YEAR, GRAPH_QL_QUERY, PUBLICATIONS, TODAY, YEARS
from ieee_csdl_downloader.data import get_pub_formats, get_pub_month
from ieee_csdl_downloader.pdf import unzip_and_merge
from ieee_csdl_downloader.publications import Publication

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def download_file(download_url: str, download_path: Optional[Path] = None) -> None:  # pragma: nocover
    if not download_path:
        download_path = Path(DOWNLOAD_DIR / download_url.split('/')[-1].split('?')[0])

    with requests.get(download_url, stream=True) as r:
        with open(download_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def get_publication_directory(pub_name: str):
    return Path(DOWNLOAD_DIR / pub_name)


def get_local_filename(
    year: int,
    month: str,
    pub_name: str,
    vol: str,
    issue: int,
    filetype: str,
    postfix: str = '',
) -> Path:
    filename = f'{year}-{month} - {pub_name} - Volume{vol} - Issue{issue}{postfix}.{filetype}'
    return get_publication_directory(pub_name) / filename


def get_publication_graphql(year: int, issue: int, publication: Publication) -> dict:  # pragma: nocover
    # GraphQL query to get the month of the publication
    r = requests.post(
        url='https://www.computer.org/csdl/api/v1/graphql',
        json={
            'operationName': None,
            'variables': {
                'announcementsCategoryId': '819',
                'cfpCategoryId': '857',
                'idPrefix': publication.url_indicator,
                'issueNum': str(issue).zfill(2),
                'year': str(year),
                'limitResults': 100,
                'skipResults': 0,
            },
            'query': GRAPH_QL_QUERY,
        },
        allow_redirects=True,
        cookies=COOKIES,
    )
    json_data = r.json()
    return json_data


def main() -> None:  # pragma: nocover
    download_problems: List[str] = []

    for pub in PUBLICATIONS:

        # Create the directory for this publication
        get_publication_directory(pub_name=pub.name).mkdir(exist_ok=True)

        # Iterate over all the desired years & issues to get the media.
        for year in YEARS or range(pub.start_year, (pub.end_year if pub.end_year else TODAY.year) + 1):

            if DOWNLOAD_START_YEAR and year < DOWNLOAD_START_YEAR:
                print(f'[{datetime.now().isoformat()}] Skipping {year} for {pub.name}; config says last download was {DOWNLOAD_START_YEAR}')
                continue

            for issue in pub.issues:
                json_data = get_publication_graphql(year=year, issue=issue, publication=pub)
                pub_month = get_pub_month(json_data=json_data)
                pub_formats = get_pub_formats(json_data=json_data)
                if not pub_month:
                    continue
                month = str(pub_month).zfill(2)

                file_fn = lambda file_type, postfix='': get_local_filename(  # noqa: E731
                    year=year,
                    month=month,
                    pub_name=pub.name,
                    vol=str(year - (pub.start_year - 1)).zfill(2),
                    issue=issue,
                    filetype=file_type,
                    postfix=postfix,
                )

                # Download each of the desired files.
                for filetype in pub_formats:
                    print(f'[{datetime.now().isoformat()}] Downloading [{pub.name}] issue ' f'for {year}-{month} (Issue {issue} - {filetype:4})...', end='')
                    url = build_download_url(pub, year, issue, filetype)

                    local_file = file_fn(file_type=filetype)

                    # Minus 1 from month because sometimes issues are published a bit early.
                    if year >= TODAY.year and int(month) - 1 > TODAY.month:
                        print('Future Issue; skipping!')
                        continue

                    if local_file.exists():
                        print('Already Downloaded; skipping!')
                        continue

                    r = requests.head(
                        url=url,
                        allow_redirects=True,
                        cookies=COOKIES,
                    )
                    if r.status_code == 403:
                        print('File does not exist; skipping!')
                        continue

                    if r.status_code != 200:
                        print('Status Code != 200; skipping!\n')
                        print('[ERROR] Please try updating the value of `CSDL_AUTH_COOKIE` and re-running the program.')
                        print('Exiting.')
                        exit(1)

                    redirected_url = r.url
                    download_file(download_url=redirected_url, download_path=local_file)
                    print('Success!')

                # If the zip file exists, but not the PDF; create zip
                pdf = file_fn(file_type='pdf')
                zip = file_fn(file_type='zip')
                if zip.exists() and not pdf.exists():
                    timestamp = datetime.now().isoformat()
                    print(f'[{timestamp}] No PDF downloaded for {year}-{month} (Issue {issue})...')
                    print(f'[{timestamp}]  \\------ extracting zip and creating...', end='')

                    merged_pdf_name = file_fn(file_type='pdf', postfix=' - MERGED_FROM_ZIP')
                    if merged_pdf_name.exists():
                        print('Merged PDF exists; skipping!')
                        continue

                    unzip_and_merge(merged_pdf_name, zip)
                    print('Success!')

    if download_problems:
        print('Problems Downloading:')
        print('===================')
        for download_problem in download_problems:
            print(f' - {download_problem}')


def build_download_url(pub, year, issue, filetype):
    url = f'https://www.computer.org/csdl/api/v1/periodical/{pub.type}/{pub.url_indicator}' f'/{year}/{str(issue).zfill(2)}/download-issue/{filetype}'
    return url


# RUN VIA: `source activate && python3 -m ieee_csdl_downloader.download && deactivate`
if __name__ == '__main__':  # pragma: nocover
    main()
