from PyInquirer import prompt


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
