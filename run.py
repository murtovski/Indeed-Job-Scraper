import requests
from bs4 import BeautifulSoup

url = "https://ie.indeed.com/jobs?q=full+stack+developer&l=Dublin%2C+County+Dublin&start=10"

result = requests.get(url)

print(result.text)