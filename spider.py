from config import *
from utilities import httpclient
from utilities import directory
from tqdm import tqdm
from PyInquirer import prompt


def search(key_word):
    '''
    Search comics by @key_word
    '''
    comics = search_comics(key_word)
    if not comics:
        return None

    selection = [
        {
            'type': 'list',
            'name': 'comics',
            'message': 'Select a comic:',
            'choices': comics.keys()
        }
    ]
    name = prompt(selection)['comics']

    return name, comics[name]


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

    with tqdm(total=total_page) as progress:
        for page in range(1, total_page + 1):
            crawl_page(page, link, volume)
            progress.update(1)


def crawl_page(page, link, volume):
    '''
    Crawl single @page and save to @volume
    '''
    url = image_url(page, link)
    filename = f'{volume}\\{page}.jpg'

    httpclient.download_file(url, filename)
