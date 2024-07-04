#!/usr/bin/env python

import urllib.parse
import requests
import json
import bs4
import os
from bs4 import BeautifulSoup


def save_content(content, company, position, count):
    directory = os.path.join(os.getcwd(), company, position)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{count}.html")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path = f"{parsed_url.path}"
    params = dict(urllib.parse.parse_qsl(parsed_url.query))
    return base_url, path, params


url = "https://banner.drexel.edu/duprod/hwczkfsea.P_StudentESaPArchiveList?i_user_type=S&i_total_recs=8795&i_recs_per_page=99&i_curr_page=1"

base_url, path, query = parseUrl(url)

session = requests.Session()
session.cookies.update({"SESSID": "Tkk3UkI2NDU1MjM0Mg=="})


companies = {}
current_company = None

for page in range(1, 90):
    query["i_curr_page"] = page

    response = session.get(base_url+path, params=query)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_data = soup.find_all('td', class_='dddefault')
    for td in table_data:
        span = td.find('span', class_='strongtext')
        a_tag: bs4.element.Tag = td.find('a')

        if span and not a_tag:
            current_company = span.get_text(strip=True)
            if current_company not in companies:
                companies[current_company] = []

        elif a_tag and current_company:  # Check for job details
            link = a_tag.get("href")
            job = a_tag.get_text(strip=True)

            response1 = session.get(base_url+link)
            soup1 = BeautifulSoup(response1.text, 'html.parser')

            table_data1 = soup1.find_all('td', class_='dddefault')

            count = 1
            for td1 in table_data1:
                a_tag: bs4.element.Tag = td.find('a')

                if a_tag:
                    href = a_tag.get('href')
                    if href:
                        full_href = urllib.parse.urljoin(base_url, href)
                        href_response = session.get(full_href)
                        save_content(href_response.text,
                                     current_company, job, count)
                        count += 1

    print(f"Page No :{page}")
