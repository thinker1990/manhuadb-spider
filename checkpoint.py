from os import path, remove
from json import dump, load


_LOG_FILE = 'PROGRESS'
_DONE = 'done'


def checkpoint_when_abort(func):
    '''
    Checkpoint when abort
    Bad smell: intimate with @func it decorated
    '''
    def wrapper(volume, link, page):
        try:
            func(volume, link, page)
        except:
            _checkpoint(volume, page)
            raise

    return wrapper


def commit_when_done(func):
    '''
    Mark as finished
    '''
    def wrapper(*args):
        func(*args)
        _checkpoint(status=_DONE)

    return wrapper


def resume_volume(func):
    '''
    Resume unprocessed volumes
    '''
    def wrapper(*args):
        volumes = func(*args)
        if not _checkpoint_exists():
            return volumes
        status, volume, _ = _progress()
        if status == _DONE:
            return []
        return _since(volume, volumes)

    return wrapper


def resume_page(func):
    '''
    Resume unprocessed pages
    '''
    def wrapper(*args):
        pages = func(*args)
        if not _checkpoint_exists():
            return pages
        _, _, abort_page = _progress()
        _complete_resume()
        return pages[abort_page-1:]

    return wrapper


def _checkpoint_exists():
    return path.exists(_LOG_FILE)


def _progress():
    with open(_LOG_FILE, 'r') as log:
        progress = load(log)
        return progress['status'], progress['volume'], progress['page']


def _checkpoint(volume='', page=0, status='abort'):
    progress = {
        'volume': volume,
        'page': page,
        'status': status
    }
    with open(_LOG_FILE, 'w') as log:
        dump(progress, log)


def _complete_resume():
    remove(_LOG_FILE)


def _since(marker, volumes: list) -> list:
    for idx, (vol, _) in enumerate(volumes):
        if vol == marker:
            return volumes[idx:]
