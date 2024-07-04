#!/usr/bin/env python

import os
import urllib.parse
import requests
import json
import time
from bs4 import BeautifulSoup


def parse_url(url):
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def save_content(content, company, position, date: str):
    directory = os.path.join(os.getcwd(), "scraped_data", company, position)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(
        directory, f"{"_".join(date.lower().split())}.html")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


url = "https://banner.drexel.edu/"
path = "/duprod/hwczkfsea.P_StudentESaPArchiveJobDisplay?i_user_type=S&i_job_num=421137&i_return=%2Fduprod%2Fhwczkfsea.P_StudentESaPArchiveList%3Fi_user_type%3DS%26i_curr_page%3D70%26i_total_recs%3D8795%26i_recs_per_page%3D99"
base_url = parse_url(url)

session = requests.Session()
session.cookies.update({"SESSID": "UTNRUkEwNDU1MjM0Mg=="})

with open('companies_test.json', 'r') as file:
    companies_data = json.load(file)

for company, positions in companies_data.items():
    print(f"--Company: {company}")
    for position in positions:
        job_name = position['name']
        link_path = position['link_path']
        full_url = urllib.parse.urljoin(base_url, link_path)
        print(f" |---Position: {job_name}")

        response = session.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table_data = soup.find_all('td', class_='ddlabel')

        for td in table_data:
            a_tag = td.find('a')
            td_text = td.get_text().replace('\n', "")
            td_text = td_text.replace("/", "_")

            print(f" |---Date: {td_text}", end="->")

            if a_tag:
                href = a_tag.get('href')
                if href:
                    print("scraped")
                    full_href = urllib.parse.urljoin(base_url, href)
                    href_response = session.get(full_href)
                    save_content(href_response.text, company,
                                 job_name, td_text)
                    break
                else:
                    print("failed")
            else:
                print("failed")
            time.sleep(.3)
