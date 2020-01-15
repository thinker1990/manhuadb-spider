import re
import requests
import os


BASE_URL = 'https://www.manhuadb.com'
VOLUME_PATTERN = r'<a class="" href="(?P<vol_url>(\w|\/)+).html" title="\S+">(?P<vol_num>\d+)</a>'
IMAGE_PATTERN = r'class="img-fluid show-pic" src="(?P<img_url>http(\w|.|\/)+.jpg)"'
PAGE_COUNT_PATTERN = r'共 (?P<total_page>\d+) 页'


def crawl(start_page, save_location):
    '''
    Crawl entire book specified by @start_page 
    and save the result to @save_location
    '''
    create_dir(save_location)
    os.chdir(save_location)  # enter the directory

    for url, num in volumes(start_page):
        crawl_volume(url, num)

    print('DONE!')


def crawl_volume(vol_url, vol_num):
    '''
    Crawl the volume specified by @vol_url and order by @vol_num
    '''
    save_location = f'vol{vol_num}'
    create_dir(save_location)

    total_page = pages_of_volume(vol_url)
    for page_num in range(1, total_page + 1):
        page_url = f'{BASE_URL}{vol_url}_p{page_num}.html'
        ok, page = get_page(page_url)
        if not ok:
            print(f'Can NOT get page: {page_url}')
            break

        image = get_image(page)
        if image is None:
            print(f'Can NOT get image: {page_url}')
            break

        filename = f'{save_location}\\{page_num}.jpg'
        save_image(image, filename)
        print(f'{filename} saved')

    print(f'Volume{vol_num} done!')


def volumes(start_page):
    '''
    Get volume list from @start_page
    Extract volumes by @VOLUME_PATTERN
    '''
    ok, page = get_page(start_page)
    if not ok:
        print(f'Can NOT get volumes: {start_page}')
        return []

    matchs = re.finditer(VOLUME_PATTERN, page)
    return [volume_info(m) for m in matchs]


def volume_info(match):
    '''
    Extract entry link and number of volume from match object
    '''
    vol_url = match.group('vol_url')
    vol_num = match.group('vol_num')
    return vol_url, vol_num


def pages_of_volume(vol_url):
    '''
    Get page count of volume specified by @vol_url
    Extract page count by @PAGE_COUNT_PATTERN
    '''
    entry_link = f'{BASE_URL}{vol_url}.html'
    ok, page = get_page(entry_link)
    if not ok:
        print(f'Can NOT get volume: {entry_link}')
        return

    total_page = extract_info(PAGE_COUNT_PATTERN, page)
    return int(total_page)


def get_page(url):
    '''
    Get HTML from @url
    '''
    response = requests.get(url)
    if response.ok:
        return True, response.text
    else:
        return False, None


def get_image(page):
    '''
    Download image of @page.
    Extract url of image by @IMAGE_PATTERN
    '''
    url = extract_info(IMAGE_PATTERN, page)
    if url is None:
        return None

    return requests.get(url)


def save_image(image, filename):
    '''
    Save @image as @filename
    '''
    with open(filename, 'wb') as fd:
        for chunk in image.iter_content():
            fd.write(chunk)


def create_dir(folder):
    '''
    Create @folder in current path.
    '''
    path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(path):
        os.mkdir(path)


def extract_info(pattern, source):
    '''
    Extract matched string specified by @pattern from @source 
    '''
    matched = re.search(pattern, source)
    if matched is None:
        return None
    m_id = re.search(r'\?P<(?P<match_id>\w+)>', pattern)
    if m_id is None:
        return matched.group(0)

    match_id = m_id.group('match_id')
    return matched.group(match_id)


if __name__ == '__main__':
    start_page = input('Enter the url of start page: ')
    save_location = input('Location to save the result: ')

    crawl(start_page, save_location)
