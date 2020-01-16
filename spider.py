from config import *
from utilities import httpclient
from utilities import directory
from tqdm import tqdm


def crawl(start_page, save_location):
    '''
    Crawl entire book specified by @start_page 
    and save the result to @save_location
    '''
    directory.create_and_cd(save_location)

    for url, num in volumes(start_page):
        crawl_volume(url, num)

    print('DONE!')


def crawl_volume(url, num):
    '''
    Crawl the volume specified by @url and order by @num
    '''
    save_location = f'volume{num}'
    directory.create(save_location)

    total_page = pages_of_volume(url)

    with tqdm(total=total_page, desc=f'Volume{num}') as progress:
        for page in range(1, total_page + 1):
            crawl_page(page, url, save_location)
            progress.update(1)


def crawl_page(page, volume, save_location):
    '''
    Crawl single @page of @volume and save to @save_location
    '''
    url = image_url(page, volume)
    filename = f'{save_location}\\{page}.jpg'

    httpclient.download_file(url, filename)
