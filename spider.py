from config import *
from checkpoint import *
from utilities import httpclient, directory, cli
from typing import Iterable


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

    @cli.progressbar(total=len(volumes), desc='Total Progress')
    def crawl_all_volumes():
        for volume, link in volumes:
            yield crawl_volume(volume, link)

    crawl_all_volumes()


def crawl_volume(volume, link):
    '''
    Crawl the @volume specified by @link
    '''
    directory.create(volume)
    pages = _get_pages(link)

    @cli.progressbar(total=len(pages), desc=volume)
    def crawl_all_pages():
        for page in pages:
            yield crawl_page(volume, link, page)

    crawl_all_pages()


@checkpoint_when_abort
def crawl_page(volume, link, page):
    '''
    Crawl single @page and save to @volume
    '''
    url = image_url(page, link)
    filename = f'{volume}\\{page}.jpg'
    httpclient.download_file(url, filename)


@resume_volume
def _get_volumes(link) -> Iterable:
    return query_volumes(link)


@resume_page
def _get_pages(link) -> Iterable:
    total_page = page_count(link)
    return range(1, total_page+1)
