from os import path, remove
from json import dump, load


LOG_FILE = 'PROGRESS'
DONE = 'done'


def mark(volume, page):
    '''
    Mark breakpoint at @page of @volume
    '''
    progress = {
        'volume': volume,
        'page': page,
        'status': 'interrupt'
    }
    with open(LOG_FILE, 'w') as log:
        dump(progress, log)


def resume_volume(volumes):
    '''
    Resume unprocessed volumes
    '''
    if not path.exists(LOG_FILE):
        return volumes

    with open(LOG_FILE, 'r') as log:
        progress = load(log)
        if progress['status'] == DONE:
            return {}
        return since(progress['volume'], volumes)


def resume_page(total_page):
    '''
    Resume unprocessed pages
    '''
    start_from = 1
    stop_at = total_page + 1

    if not path.exists(LOG_FILE):
        return range(start_from, stop_at)

    with open(LOG_FILE, 'r') as log:
        progress = load(log)
        start_from = progress['page']

    remove(LOG_FILE)  # resume complete
    return range(start_from, stop_at)


def commit():
    '''
    Mark as finished
    '''
    with open(LOG_FILE, 'w') as log:
        dump({'status': DONE}, log)


def since(marker, volumes):
    '''
    Filter unprocessed @volumes since @marker
    '''
    not_processed = {}
    match = False
    for key, val in volumes.items():
        if match:
            not_processed[key] = val
        elif key == marker:
            not_processed[key] = val
            match = True

    return not_processed
