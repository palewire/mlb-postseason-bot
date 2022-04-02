import json

import click
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


@click.group()
def cli():
    """Scrape data."""
    pass


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
