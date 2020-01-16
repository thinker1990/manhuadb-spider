from utilities import httpclient
from utilities import regex


BASE_URL = "https://www.manhuadb.com"

VOLUME_PATTERN = r'<a class="" href="(?P<vol_url>(?:\w|/)+).html" title=".+">(?P<vol_num>\d+)</a>'
IMAGE_PATTERN = r'class="img-fluid show-pic" src="(?P<img_url>http(\w|.|/)+.jpg)"'
PAGE_COUNT_PATTERN = r"共 (?P<total_page>\d+) 页"


def volumes(entry_link):
    """
    Get volume list from @entry_link
    """
    start_url = f'{BASE_URL}{entry_link}'
    page = httpclient.get_page(start_url)

    return regex.multi_match(VOLUME_PATTERN, page)


def page_count(vol_url):
    """
    Get page count of volume specified by @vol_url
    Extract page count by @PAGE_COUNT_PATTERN
    """
    entry_link = f"{BASE_URL}{vol_url}.html"
    page = httpclient.get_page(entry_link)

    total_page = regex.extract(PAGE_COUNT_PATTERN, page)
    return int(total_page)


def image_url(page, volume):
    '''
    Get image url of @page from @volume
    '''
    url = f'{BASE_URL}{volume}_p{page}.html'
    page_html = httpclient.get_page(url)

    return regex.extract(IMAGE_PATTERN, page_html)
