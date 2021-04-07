import string
import requests
from bs4 import BeautifulSoup


def web_scraper():
    """Implementation of stage 4/5 web scraper"""
    url = "https://www.nature.com/nature/articles"
    articles = article_checker(request_getter(url))
    for arty in articles.values():
        if arty[0] == "News":
            page = request_getter(url[:-16] + arty[1])  # -16 to get www.nature.com/articles/<id>
            content_extractor(page)


def article_checker(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    dict_of_art = {}  # Dictionary used for storing article {'id' : [type, link]}
    i = 0  # counter which works as the key for the current article
    for article in soup.find_all("article"):
        art_type = article.find("span", attrs={"data-test": "article.type"})
        art_href = article.find("a", attrs={"data-track-action": "view article"}).get('href')
        dict_of_art[i] = []
        dict_of_art[i].append(art_type.find("span").contents[0])
        dict_of_art[i].append(art_href)
        i += 1
    return dict_of_art


def content_extractor(page):
    """Extracts content from nature.com website."""
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("head").find("title").contents  # Finds the title of the page
    # String processing of the title, getting rid of punctuation
    fn = title[0].rstrip().translate(str.maketrans('', '', string.punctuation))
    file_name = fn.replace(' ', '_')  # Final string processing in order to use the title as filename
    article_content = soup.find("body").find("div", attrs={"class": "article__body cleared"}).find_all(["p", "h2", "h3", "h4"])
    content_encoded = b''
    for paragraph in article_content:
        if not paragraph.has_attr("class") or "recommended__title" not in paragraph.attrs["class"]:
            content_encoded += paragraph.text.encode('utf-8')
    content_saver(file_name, content_encoded)


def request_getter(url):
    """Getting"""
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})  # Forces English version of the page
    if r.status_code != 200:
        print("The URL returned {}!".format(r.status_code))
        return 0
    else:
        return r


def content_saver(file_name, content):
    """Writing the content of a tag into a binary file"""
    with open('{}.txt'.format(file_name), 'wb') as file:
        file.write(content)
        print(file_name, "has been saved!")


def main():
    web_scraper()


if __name__ == '__main__':
    main()
