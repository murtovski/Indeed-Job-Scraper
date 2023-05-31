import requests
from bs4 import BeautifulSoup

def get_role(role):
    
    role = role.replace(" ", "+")


def extract(page):
    url = f'https://www.jobs.ie/Jobs.aspx?hd_searchbutton=true&Keywords={role}&Regions=0&Categories=0&job-search=true'
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    result = requests.get(url, header)
    doc = BeautifulSoup(result.content, "html.parser")
    return doc


def filter_information(doc):
    titles = doc.find_all('div', class_='job-details-header')
    for item in titles:
        title = item.find('h2').text
        company = item.find('text', class_='company-title-name').text.strip()
        location = item.find('dd', class_='fa-map-marker').text.strip()
        full_job = {
            'Title': title, 
            'Company': company,
            'Location': location
        }
        list.append(full_job)
    return


def main():
    role = input("Please enter the role in which you would like to search. ")
    get_role(role)
    list = []
    info = extract(0)
    filter_information(info)
    for item in list:
        print(item)
        
    
main()