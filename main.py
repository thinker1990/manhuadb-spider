from spider import search, crawl


if __name__ == "__main__":
    key_word = input("Enter comic name: ")
    result = search(key_word)
    if not result:
        print('No item found')

    comic, link = result
    confirm = input(f'Download {comic} now? (Yes/No): ')
    if confirm.upper().startswith('Y'):
        crawl(comic, link)
        print('DONE!')
