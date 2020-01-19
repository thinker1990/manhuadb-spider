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


def progressbar(func):
    '''
    Decorate the @tasks with progress bar
    '''
    def wrapper(items: Iterable, task):
        iterable_tasks = func(items, task)
        for i in tqdm(iterable_tasks, total=len(items)):
            pass
    return wrapper
