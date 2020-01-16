import spider
from utilities import httpclient
from utilities import regex
from bullet import Bullet


BOOK_LIST_PATTERN = r'<a href="(?P<comic_url>(?:\w|/)+)" title="(?P<comic_name>.+)" class="d-block">'


# 1 input key word:
key_word = print("Enter comic name: ")
# 2 search result:
search_url = f"{spider.BASE_URL}/search?q={key_word}"
result = httpclient.get_page(search_url)
book_list = regex.multi_match(BOOK_LIST_PATTERN, result)
book_dir = {title: url for url, title in book_list}
cli = Bullet(prompt="Please choose one to download: ", choices=book_dir.keys)

result = cli.launch()
print("You chose:", result, book_dir[result])

start_page = f"{spider.BASE_URL}{book_dir[result]}"
save_location = result
spider.crawl(start_page, save_location)


if __name__ == "__main__":
    start_page = input("Enter the url of start page: ")
    save_location = input("Location to save the result: ")

    spider.crawl(start_page, save_location)
