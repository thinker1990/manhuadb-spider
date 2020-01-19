from config import *
from checkpoint import *
from utilities import httpclient, directory, cli


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

    @cli.progressbar
    def process_each(items):
        for volume, link in items:
            yield crawl_volume(volume, link)
    process_each(volumes)


def crawl_volume(volume, link):
    '''
    Crawl the @volume specified by @link
    '''
    directory.create(volume)
    pages = _get_pages(link)

    @cli.progressbar
    def process_each(items):
        for page in items:
            yield crawl_page(volume, link, page)
    process_each(pages)


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
