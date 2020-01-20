from PyInquirer import prompt
from tqdm import tqdm
from typing import Iterable


def select(choices) -> str:
    '''
    Choose one from @choices
    '''
    _choices = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'Please choose one:',
            'choices': choices
        }
    ]

    return prompt(_choices)['choice']


def confirm(question) -> bool:
    '''
    Confirm @question
    '''
    _question = [
        {
            'type': 'confirm',
            'name': 'answer',
            'message': question,
            'default': True
        }
    ]

    return prompt(_question)['answer']


def progressbar(total, desc=None):
    '''
    Decorate the tasks with progress bar
    '''
    def pbar_decorator(func):
        def wrapper(*args):
            tasks = func(*args)
            for i in tqdm(tasks, desc, total):
                pass
        return wrapper

    return pbar_decorator
