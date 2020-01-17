from tqdm import tqdm


def decorate(iterable_task, total):
    '''
    Decorate the @iterable_task with progress bar
    '''
    for i in tqdm(iterable_task, total=total):
        pass
