import string
import os
import requests
from bs4 import BeautifulSoup


def web_scraper():
    """Implementation of stage 5/5 web scraper"""
    basic_url = "https://www.nature.com/nature/articles/?searchType=journalSearch&sort=PubDate&page="
    list_of_urls = []   # list of pages listing articles
    how_many_pages = int(input())
    if how_many_pages < 1:
        print("invalid number of pages! Fetching results for just one page...")
    elif how_many_pages >= 1:
        for i in range(1, how_many_pages + 1):
            directory = "Page_" + str(i)
            list_of_urls.append(basic_url + str(i))
            if not os.access(directory, os.F_OK):    # checking if the directory exists
                os.makedirs(directory)
    desired_type = input()
    articles = article_checker(list_of_urls, desired_type)
    for arty in articles.values():
        page = request_getter("https://www.nature.com" + arty[1])
        content_extractor(page, arty[2])


def article_checker(urls, desired_type):
    """Looks up each article listing page for articles of a desired type"""
    articles_dict = {}  # For storing articles {'id' : [type, link, page_no]}
    i = 0  # Counter - the key for the current article
    page_no = 1         # Number of current articles listing page, for creating directories later on
    for url in urls:
        page = request_getter(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for article in soup.find_all("article"):
            art_type = article.find("span", attrs={"data-test": "article.type"}).find("span").contents[0]
            art_href = article.find("a", attrs={"data-track-action": "view article"}).get('href')
            if art_type == desired_type:
                articles_dict[i] = []
                articles_dict[i].append(art_type)
                articles_dict[i].append(art_href)
                articles_dict[i].append(page_no)
                i += 1
        page_no += 1
    return articles_dict


def content_extractor(page, page_number):
    """Extracts content from nature.com website."""
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("head").find("meta", attrs={"property": "og:title"}).get("content")  # Finds the title of the page
    # String processing of the title, getting rid of punctuation
    file_name = string_processing(title)
    article_content = soup.body.find("div", attrs={"class": "article-item__body"})
    if not article_content:
        article_content = soup.body.find("div", attrs={"itemprop": "articleBody"})
    real_content = article_content.find_all(["p", "h1", "h2", "h3", "h4"])
    content_encoded = b''
    for paragraph in real_content:
        if not paragraph.has_attr("class") or "recommended__title" not in paragraph.attrs["class"]:
            content_encoded += paragraph.text.encode('utf-8')

    directory = "Page_" + str(page_number)
    content_saver(directory + "/" + file_name + ".txt", content_encoded)


def request_getter(url):
    """Getting the url or returning 0"""
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})  # Forces English version of the page
    if r.status_code != 200:
        print("The URL returned {}!".format(r.status_code))
        return 0
    else:
        return r


def string_processing(title_string):
    no_punctuation = title_string.rstrip().translate(str.maketrans('', '', string.punctuation))
    return no_punctuation.replace(' ', '_')


def content_saver(path, content):
    """Writing the content of a tag into a binary file"""
    with open(path, 'wb') as file:
        file.write(content)
        print(path, "has been created!")


def main():
    web_scraper()


if __name__ == '__main__':
    main()
