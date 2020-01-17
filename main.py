from spider import search, crawl
from utilities.prompt import *
import sys


if __name__ == '__main__':
    key_word = input('Enter comic name: ')
    comics = search(key_word)
    if not comics:
        print('No item found')
        sys.exit()

    name = select(comics.keys())
    comic, link = name, comics[name]
    ready = confirm(f'Download {comic} now?')
    if ready:
        crawl(comic, link)

    print('DONE!')
