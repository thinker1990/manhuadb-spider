from tqdm import tqdm
from typing import Iterable


def decorate(tasks: Iterable, count: int):
    '''
    Decorate the @tasks with progress bar
    '''
    for i in tqdm(tasks, total=count):
        pass
