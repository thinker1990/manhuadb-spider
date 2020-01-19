from utilities import httpclient, regex


BASE_URL = "https://www.manhuadb.com"

COMIC_PATTERN = r'<a href="(?P<link>(?:\w|/)+)" title="(?P<comic>.+)" class="d-block">'
VOLUME_PATTERN = r'href="(?P<link>(?:\w|/)+).html" title="(?P<volume>.+)"'
PAGE_COUNT_PATTERN = r"共 (?P<page_count>\d+) 页"
IMAGE_PATTERN = r'class="img-fluid show-pic" src="(?P<image>http(\w|.|/)+.jpg)"'


def query_comics(key_word) -> dict:
    '''
    Search comics by @key_word
    '''
    query = f"{BASE_URL}/search?q={key_word}"
    result = httpclient.get_page(query)
    comics = regex.multi_match(COMIC_PATTERN, result)

    return {comic: link for link, comic in comics}


def query_volumes(entry_link) -> list:
    """
    Query volume list from @entry_link
    """
    url = f'{BASE_URL}{entry_link}'
    page = httpclient.get_page(url)

    volumes = regex.multi_match(VOLUME_PATTERN, page)
    return [(volume, link) for link, volume in volumes]


def page_count(entry_link) -> int:
    """
    Get page count of volume specified by @entry_link
    """
    url = f"{BASE_URL}{entry_link}.html"
    page = httpclient.get_page(url)

    count = regex.extract(PAGE_COUNT_PATTERN, page)
    return int(count)


def image_url(page, entry_link) -> str:
    '''
    Get image url of @page derived from @entry_link
    '''
    url = f'{BASE_URL}{entry_link}_p{page}.html'
    page_html = httpclient.get_page(url)

    return regex.extract(IMAGE_PATTERN, page_html)
