from datetime import date
from pathlib import Path

from ieee_csdl_downloader.publications import Publication

DEBUG = False
TODAY = date.today()

GRAPH_QL_QUERY = (
    """query ($idPrefix: String!, $year: String!, $issueNum: String!, $cfpCategoryId: String!, $announcementsCategoryId: String!, $limitResults: Int, $skipResults: Int) {   # noqa: E501
    issue: periodicalIssue(idPrefix: $idPrefix, year: $year, issueNum: $issueNum) {
        id
        idPrefix
        isPreviewOnly
        issueNum
        pubType
        hideFullIssueDownloadButton
        downloadables {
            hasCover
            hasAzw3
            hasEpub
            hasMathEpub
            hasMobi
            hasPdf
            hasZip
            __typename
        }
        title
        label
        volume
        year
        colloquiumHtmlIssue {
            isHtmlFormat
            issueArray {
                title
                year
                issueNum
                idPrefix
                volume
                label
                __typename
            }
            __typename
        }
        __typename
    }
    articles: articlesWithPagination(idPrefix: $idPrefix, year: $year, issueNum: $issueNum, limit: $limitResults, skip: $skipResults) {
        skipped
        limit
        totalResults
        articleResults {
            id
            authors {
                fullName
                givenName
                surname
                __typename
            }
            replicability {
                isEnabled
                codeRepositoryUrl
                codeDownloadUrl
                __typename
            }
            fno
            isOpenAccess
            issueNum
            sectionTitle
            title
            year
            pages
            pubType
            pubDate
            doi
            idPrefix
            __typename
        }
        __typename
    }
    trendingArticles: popularArticlesByPeriodical(idPrefix: $idPrefix) {
        id
        doi
        title
        authors {
            givenName
            surname
            fullName
            __typename
        }
        pages
        year
        pubType
        idPrefix
        issueNum
        year
        fno
        __typename
    }
    announcements: wordpressContent(categoryId: $announcementsCategoryId) {
        id
        title
        url
        __typename
    }
    callForPapers: callForPapers(categoryId: $cfpCategoryId) {
        id
        title
        url
        __typename
    }
}
"""
    ''
)

PUBLICATIONS = [
    # Publication(name='IEEE Cloud Computing', type='mags', url_indicator='cd', start_year=2014, end_year=2018),
    # Publication(name='IEEE Concurrency', type='mags', url_indicator='cd', start_year=1993, end_year=2000),
    # Publication(name='IEEE Design & Test of Computers', type='mags', url_indicator='dt', start_year=1984, end_year=2014),
    # Publication(name='IEEE Distributed Systems Online', type='mags', url_indicator='dt', start_year=2000, end_year=2008),
    Publication(name='IEEE Security & Privacy', type='mags', url_indicator='sp', start_year=2003, end_year=None),
    Publication(name='IEEE Transactions on Big Data', type='trans', url_indicator='bd', start_year=2015, end_year=None),
]

if DEBUG:  # pragma: nocover
    DOWNLOAD_DIR = Path('./downloads_debug')
    YEARS = [2022]
    ISSUES = [1, 2, 3, 4, 5, 6]
else:
    DOWNLOAD_DIR = Path('./downloads')
    YEARS = []
    ISSUES = [1, 2, 3, 4, 5, 6]
