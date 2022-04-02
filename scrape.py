import json

import click
from bs4 import BeautifulSoup
from dateutil import parser as dateparse
from playwright.sync_api import sync_playwright
import requests


@click.group()
def cli():
    """Scrape data."""
    pass


@cli.command()
def schedule():
    """Scrape schedules from Baseball Reference."""
    # Get the page
    url = "https://www.baseball-reference.com/teams/CHC/2022-schedule-scores.shtml"
    r = requests.get(url)

    # Parse it
    soup = BeautifulSoup(r.text, "html5lib")

    # Grab the table
    table = soup.find("table", class_="stats_table")

    # Loop through each row
    row_list = []
    for row in table.find_all("tr")[1:-1]:
        d = {}
        # Get the cells
        cell_list = row.find_all(['td', 'th'])

        # Skip the cruft rows
        if cell_list[0].text == "Gm#":
            continue

        # Pull the data
        for cell in cell_list:
            d[cell.attrs['data-stat']] = cell.text

        # Parse the dates
        d['date'] = dateparse.parse(d['date_game'] + " 2022")

        # Add them to the list
        row_list.append(d)

    # Write it out
    with open("./data/schedule.json", "w") as fp:
        json.dump(row_list, fp, indent=2, sort_keys=True, default=str)


@cli.command()
def fangraphs():
    """Scrape playoff odds from fangraphs."""
    with sync_playwright() as p:
        # Open the browser
        browser_obj = p.chromium.launch()

        # Get the page
        page = browser_obj.new_page()
        page.goto("https://www.fangraphs.com/standings/playoff-odds")

        # Pull the html
        html = page.content()

    # Parse the HTML
    soup = BeautifulSoup(html, "html5lib")

    # Pull out the tables
    table_list = soup.find_all("table", class_="playoff-odds-table")
    team_dict = {}

    # Loop through them
    for table in table_list:
        tbody = table.tbody
        tr_list = tbody.find_all("tr")
        # Go through the rows
        for row in tr_list:
            # Pull out the column want
            name = row.find("span", class_="fullName").text
            team_dict[name] = float(row.find("td", class_="highlight-sort").text.replace("%", ""))

    # Write it out
    with open("./data/fangraphs.json", "w") as fp:
        json.dump(team_dict, fp, indent=2, sort_keys=True)


if __name__ == "__main__":
    cli()
