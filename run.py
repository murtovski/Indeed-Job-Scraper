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
MAX_CALLS = 60
job_list = []


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
        job_list.append(full_job)
    return


def check_next_empty(worksheet):
    values_list = worksheet.col_values(1)
    next_row = len(values_list) + 1
    print(next_row)
    return next_row
        

def update_sheet(entry):
    worksheet = sheet.worksheet('Sheet1')
    next_row = check_next_empty(worksheet)
    next_col = 2
    today = date.today().isoformat()
    worksheet.update(f'A{next_row}', today)
    worksheet.update(f'B{next_row}', f'Search: {entry}')
    for item in job_list:
        index = 0
        full_string = f"Title: {item['Title']}\nCompany: {item['Company']}\nLocation: {item['Location']}"
        div, mod = divmod(next_col, len(ALPHABET))  # Updated 'i' to 'next_row'
        column = ALPHABET[div - 1] + ALPHABET[mod] if div > 0 else ALPHABET[mod]
        cell_range = f"{column}{next_row}"
        worksheet.update(cell_range, full_string)
        next_col += 1
        print(full_string)
        print()
        index += 1
        if index >= 55:
            break
        
    
def main():
    entry = input("Please enter the role in which you would like to search. ")
    role = get_role(entry)
    info = extract(0, role)
    filter_information(info)
    update_sheet(entry)
    

main()