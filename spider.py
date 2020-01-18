from config import *
import checkpoint
from utilities import httpclient, directory, cli


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
    volumes = checkpoint.resume_volume(volumes)

    def tasks():
        for volume, link in volumes.items():
            yield crawl_volume(volume, link)

    cli.progressbar(tasks(), len(volumes), desc='Total Progress')
    checkpoint.commit()


def crawl_volume(volume, link):
    '''
    Crawl the @volume specified by @link
    '''
    directory.create(volume)
    pages = checkpoint.resume_page(page_count(link))

    def tasks():
        for page in pages:
            yield crawl_page(page, link, volume)

    cli.progressbar(tasks(), len(pages))


def crawl_page(page, link, volume):
    '''
    Crawl single @page and save to @volume
    '''
    try:
        url = image_url(page, link)
        filename = f'{volume}\\{page}.jpg'
        httpclient.download_file(url, filename)
    except:
        checkpoint.mark(volume, page)
        raise
