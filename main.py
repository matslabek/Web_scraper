import requests
from bs4 import BeautifulSoup


def web_scraper():
    user_url = input("Input the URL:")
    response = request_getter(user_url)
    if response:
        print(response)


def request_getter(url):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code != 200:
        print("Invalid movie page!")
        return 0
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        if soup.find("meta", attrs={"property": "og:site_name"})['content'] != 'IMDb':
            print("Invalid movie page!")
            return 0
    except TypeError:
        print('Invalid movie page!')
        return 0
    accepted_types = ['video.movie', 'video.tv_show']
    if soup.find("meta", attrs={"property": "og:type"})['content'] not in accepted_types:
        print("Invalid movie page!")
        return 0
    title = soup.find("meta", attrs={'name': 'title'})
    description = soup.find("meta", attrs={'name': 'description'})

    return {"title": title['content'], "description": description['content']}


def main():
    web_scraper()


if __name__ == '__main__':
    main()