from config import *
from utilities import httpclient
from utilities import directory
from utilities import progressbar


def search(key_word):
    '''
    Search comics by @key_word
    '''
    return query_comics(key_word)


def crawl(comic, start_page):
    '''
    Crawl @comic specified by @start_page 
    '''
    directory.create_and_cd(comic)

    volumes = get_volumes(start_page)
    for volume, link in volumes.items():
        crawl_volume(volume, link)


def crawl_volume(volume, link):
    '''
    Crawl the @volume specified by @link
    '''
    directory.create(volume)
    total_page = page_count(link)

    def tasks():
        for idx in range(total_page):
            yield crawl_page(idx, link, volume)

    progressbar.decorate(tasks(), total_page)


def crawl_page(index, link, volume):
    '''
    Crawl single page specified by @index and save to @volume
    '''
    page = index + 1  # index is zero based
    url = image_url(page, link)
    filename = f'{volume}\\{page}.jpg'

    httpclient.download_file(url, filename)
