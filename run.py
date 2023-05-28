import requests
from bs4 import BeautifulSoup


def extract(page):
    url = f"https://ie.indeed.com/jobs?q=full+stack+developer&l=Dublin%2C+County+Dublin&start={page}"
    result = requests.get(url)
    doc = BeautifulSoup(result.content, "html.parser")
    return doc


def filter_information(doc):
    titles = doc.find_all('div', class_='jobTitle')
    for item in titles:
        title = item.find('a').text
        print(title)
    return


info = extract(0)
filter_information(info)