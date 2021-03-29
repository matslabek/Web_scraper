import requests


def web_scraper():
    user_url = input("Input the URL:")
    response = request_getter(user_url)


def request_getter(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Invalid quote resource!")
        return 0
    content = r.json()['content']
    if content:
        print(content)
    else:
        print("Invalid quote resource!")
        return 0
    return r


web_scraper()
