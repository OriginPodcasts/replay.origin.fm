import re
import requests


ITUNES_STORE_URL_PATTERNS = (
    r'^https?:\/\/(?:.+\.)?itunes\.apple\.com\/.+\/podcast\/.+\/id(\d+)',
    r'^https?:\/\/itunes\.apple\.com\/(?:[\a-z]{2}\/)?podcast\/(?:[\w-])+\/id(\d+)',  # NOQA
    r'^https?:\/\/itunes\.apple\.com\/(?:[\a-z]{2}\/)?podcast\/id(\d+)',
    r'^https?:\/\/podcasts\.apple\.com\/(?:.+\/)?podcast\/(?:.+\/)?(?:id)?(\d+)',  # NOQA
    r'^https?:\/\/pcr\.apple\.com\/id(\d+)'
)

ITUNES_LOOKUP_API_URL = 'https://itunes.apple.com/lookup'


def find(url):
    for regex in ITUNES_STORE_URL_PATTERNS:
        matches = re.search(regex, url)
        if matches is None:  # pragma: no cover
            continue

        itunes_id = matches.groups()[0]
        response = requests.get(
            ITUNES_LOOKUP_API_URL,
            params=dict(
                id=itunes_id,
                media='podcast',
                entity='podcast',
                limit=1
            )
        )

        data = response.json()
        for result in data.get('results', []):
            return result['feedUrl']
