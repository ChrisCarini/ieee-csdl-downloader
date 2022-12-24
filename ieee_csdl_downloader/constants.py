from datetime import date

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
