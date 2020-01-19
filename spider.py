from config import *
from checkpoint import *
from utilities import httpclient, directory, cli
from typing import Iterable, Callable


def search(key_word):
    '''
    Search comics by @key_word
    '''
    return query_comics(key_word)


@commit_when_done
def crawl(comic, start_page):
    '''
    Crawl @comic specified by @start_page 
    '''
    directory.create_and_cd(comic)

    volumes = _get_volumes(start_page)
    _iterate_over(volumes, crawl_volume)


def crawl_volume(volume, link):
    '''
    Crawl the @volume specified by @link
    '''
    def _crawl_page(page):
        crawl_page(volume, link, page)

    directory.create(volume)

    pages = _get_pages(link)
    _iterate_over(pages, _crawl_page)


@checkpoint_when_abort
def crawl_page(volume, link, page):
    '''
    Crawl single @page and save to @volume
    '''
    url = image_url(page, link)
    filename = f'{volume}\\{page}.jpg'
    httpclient.download_file(url, filename)


@resume_volume
def _get_volumes(link):
    return query_volumes(link)


@resume_page
def _get_pages(link):
    return page_count(link)


@cli.progressbar
def _iterate_over(items: Iterable, task: Callable):
    for item in items:
        yield task(item)
