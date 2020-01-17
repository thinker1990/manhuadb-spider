import requests
import tenacity
from tenacity import retry


STOP_CONDITION = tenacity.stop_after_attempt(3)
WAIT_INTERVAL = tenacity.wait_random(min=3, max=5)


@retry(stop=STOP_CONDITION, wait=WAIT_INTERVAL)
def get_page(url):
    '''
    Get HTML from @url
    '''
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        raise Exception(f'Can NOT get page: {url}')


@retry(stop=STOP_CONDITION, wait=WAIT_INTERVAL)
def download_file(url, save_as):
    '''
    Download file from @url and save as @save_as
    '''
    response = requests.get(url, stream=True)
    if not response.ok:
        raise Exception(f'Can NOT download file: {url}')

    with open(save_as, 'wb') as fd:
        for chunk in response.iter_content():
            fd.write(chunk)
