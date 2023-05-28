import requests
from bs4 import BeautifulSoup


def extract(page):
    url = f'https://ie.indeed.com/jobs?q=full+stack+developer&l=Dublin%2C+County+Dublin&start={page}'
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    result = requests.get(url, header)
    doc = BeautifulSoup(result.content, "html.parser")
    return result.status_code


def filter_information(doc):
    titles = doc.find_all('div', class_='cardOutline')
    return len(titles)


info = extract(0)
print(info)
#print(filter_information(info))