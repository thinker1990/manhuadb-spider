import os


def create(folder):
    '''
    Create @folder in current path.
    '''
    path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(path):
        os.mkdir(path)


def create_and_cd(folder):
    '''
    Create @folder and change directory to id.
    '''
    create(folder)
    os.chdir(folder)
