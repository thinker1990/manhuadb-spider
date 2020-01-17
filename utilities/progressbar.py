from tqdm import tqdm
from typing import Iterable


def decorate(tasks: Iterable, count: int, desc=None):
    '''
    Decorate the @tasks with progress bar
    '''
    for i in tqdm(tasks, desc, count):
        pass
