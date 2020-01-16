from utilities import httpclient
from utilities import regex
from utilities import directory
from tqdm import tqdm


BASE_URL = 'https://www.manhuadb.com'
VOLUME_PATTERN = r'<a class="" href="(?P<vol_url>(?:\w|\/)+).html" title="\S+">(?P<vol_num>\d+)</a>'
IMAGE_PATTERN = r'class="img-fluid show-pic" src="(?P<img_url>http(\w|.|\/)+.jpg)"'
PAGE_COUNT_PATTERN = r'共 (?P<total_page>\d+) 页'


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
    url = f'{BASE_URL}{volume}_p{page}.html'
    page_html = httpclient.get_page(url)

    image_url = regex.extract(IMAGE_PATTERN, page_html)
    filename = f'{save_location}\\{page}.jpg'

    httpclient.download_file(image_url, filename)


def volumes(start_page):
    '''
    Get volume list from @start_page
    Extract volumes by @VOLUME_PATTERN
    '''
    page = httpclient.get_page(start_page)
    return regex.multi_match(VOLUME_PATTERN, page)


def pages_of_volume(vol_url):
    '''
    Get page count of volume specified by @vol_url
    Extract page count by @PAGE_COUNT_PATTERN
    '''
    entry_link = f'{BASE_URL}{vol_url}.html'
    page = httpclient.get_page(entry_link)

    total_page = regex.extract(PAGE_COUNT_PATTERN, page)
    return int(total_page)


if __name__ == '__main__':
    start_page = input('Enter the url of start page: ')
    save_location = input('Location to save the result: ')

    crawl(start_page, save_location)
