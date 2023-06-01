import gspread
from google.oauth2.service_account import Credentials
import requests
from bs4 import BeautifulSoup
from datetime import date
import string


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

ALPHABET = string.ascii_uppercase
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
sheet = GSPREAD_CLIENT.open('Jobs-Scraper')


list = []


def get_role(role):
    if not role.isdigit():
        role = role.strip()
        role = role.replace(" ", "+")
    else:
        print("Jobs can not be numbers.")
    return role
        

def extract(page, role):
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


def format_jobs(entry):
    worksheet = sheet.get_worksheet(0)
    values = worksheet.get_all_values()
    next_row = len(values) + 1
    today = date.today()
    worksheet.update(f'A{next_row}', today)
    worksheet.update(f'B{next_row}', f'Search: {entry}')
    for item in list:
        full_string = f"Title: {item['Title']} \n Company: {item['Company']} \n Location: {item['Location']}"
        for i, value in enumerate(full_string):
            cell_range = f"{ALPHABET[i]}{next_row}"
            worksheet.update(cell_range, value)
        # worksheet.update(f'A{next_row}:C{next_row}', [full_string])
        print(f"Title: {item['Title']}")
        print(f"Company: {item['Company']}")
        print(f"Location: {item['Location']}")
        print()


def main():
    entry = input("Please enter the role in which you would like to search. ")
    role = get_role(entry)
    info = extract(0, role)
    filter_information(info)
    format_jobs(entry)
    

main()