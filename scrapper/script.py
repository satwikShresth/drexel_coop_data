#!/usr/bin/env python

import urllib.parse
import requests
import json
from bs4 import BeautifulSoup


def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    params = dict(urllib.parse.parse_qsl(parsed_url.query))
    return base_url, params


url = "https://banner.drexel.edu/duprod/hwczkfsea.P_StudentESaPArchiveList?i_user_type=S&i_total_recs=8795&i_recs_per_page=99&i_curr_page=1"

base_url, query = parseUrl(url)

session = requests.Session()
session.cookies.update({"SESSID": "TkhERUgzNDU1MjM0Mg=="})


companies = {}
current_company = None

for page in range(1, 90):
    query["i_curr_page"] = page

    response = session.get(base_url, params=query)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_data = soup.find_all('td', class_='dddefault')
    for td in table_data:
        a_tag = td.find('a')
        span = td.find('span', class_='strongtext')

        if span and not a_tag:  # Check for company name
            current_company = span.get_text(strip=True)
            if current_company not in companies:
                companies[current_company] = []
        elif a_tag and current_company:  # Check for job details
            job = a_tag.get_text(strip=True)
            companies[current_company].append(job)

    print(f"Page No :{page}")

    with open('companies_2nd_try.json', 'w+') as file:
        json.dump(companies, file, indent=4)
