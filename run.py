import requests
from bs4 import BeautifulSoup


def extract(page):
    url = f"https://ie.indeed.com/jobs?q=full+stack+developer&l=Dublin%2C+County+Dublin&start={page}"
    result = requests.get(url)
    doc = BeautifulSoup(result.content, "html.parser")
    return doc


info = extract(0)
print(info.prettify())