import requests


def get_page(url):
    '''
    Get HTML from @url
    '''
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        raise Exception(f'Can NOT get page: {url}')


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
