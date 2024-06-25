import ast

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.crawler.crawler_utilities import *

# %% Get the list of URLs to scrape

BASE_URL = "https://en.wikipedia.org"
INDEX_URL = f"{BASE_URL}/wiki/List_of_computer_scientists"

response = requests.get(INDEX_URL)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find(id="mw-content-text").find_all("li")

urls = []

for line in links:
    link = line.find("a")

    # Keep only links that refer to Wikipedia articles
    if link['href'].find("/wiki/") == -1:
        continue

    # Stop when we reach the "Lists portal" link
    if link.text == "Lists portal":
        break

    # Construct the full URL and add it to the list
    urls.append(BASE_URL + link['href'])

print(f"Found {len(urls)} valid URLs to scrape.")

# %% Scrap the raw data from the Wikipedia pages

df = pd.DataFrame(columns=["name", "education", "alma_mater", "awards"])

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    name = soup.find(id="firstHeading").string
    education = []
    alma_mater = []
    awards = []

    # Try to find the infobox
    infobox = soup.find("table", {"class": "infobox"})

    if infobox:
        # Find all the table rows that contain a table header
        tr_list = infobox.select('tr:has(th.infobox-label)')

        for tr in tr_list:
            th = tr.find("th", {"class": "infobox-label"})
            th_text = normalize_text(th.get_text()).lower()

            if th_text == 'education':
                education = education + [i.text for i in tr.find_all("a")]
            if th_text == 'alma mater':
                alma_mater = alma_mater + [i.text for i in tr.find_all("a")]
            if th_text == 'awards':
                awards = awards + [i.text for i in tr.find_all("a")]

    df.loc[len(df)] = [name, education, alma_mater, awards]

    display_progress_bar(len(df), len(urls))

df.to_csv(f"data/computer_scientists.raw.csv", index=False)

# %% Process the raw data & save it to a CSV file

df = pd.read_csv(f"data/computer_scientists.raw.csv")

df["name"] = df["name"].apply(normalize_text).apply(remove_text_in_parentheses)
df["alma_mater"] = df["alma_mater"].apply(ast.literal_eval).apply(exclude_degree_titles).apply(exclude_references)
df["education"] = df["education"].apply(ast.literal_eval).apply(exclude_degree_titles).apply(exclude_references)
df["awards"] = df["awards"].apply(ast.literal_eval).apply(exclude_references)

df["education"] = df["education"] + df["alma_mater"]
df.drop(columns=["alma_mater"], inplace=True)

df.to_csv(f"data/computer_scientists.pp.csv", index=False)
