from datetime import datetime
import json
import os

import click
from dateutil import parser as dateparse
import twitter


@click.group
def cli():
    """Tweet the latest data."""
    pass


@cli.command()
def cubs():
    """Post the latest data."""
    # Open the data
    standings = json.load(open("./data/standings.json", "r"))
    team_standings = next(t for t in standings['205']['teams'] if t['name'] == 'Chicago Cubs')

    schedule = json.load(open("./data/schedule.json", "r"))
    games_left = [g for g in schedule if not hasattr(g, "win_loss_result")]
    until_deadline = [g for g in games_left if dateparse.parse(g['date']) < datetime(2022, 8, 4)]

    projections = json.load(open("./data/fangraphs.json", "r"))

    # Format the message
    message = f"""⚾🧮 @Cubs Postseason Update 🧮⚾

{team_standings['w']} wins
{team_standings['l']} losses

{len(games_left)} games left
{len(until_deadline)} games until the Aug. 3 trade deadline

{projections['Cubs']}% chance of making the playoffs, according to @fangraphs
"""

    # Tweet it
    api = get_twitter_client()
    status = api.PostUpdate(message)


def get_twitter_client():
    """Return a Twitter client ready to post to the API."""
    return twitter.Api(
        consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token_key=os.getenv("TWITTER_ACCESS_TOKEN_KEY"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )


if __name__ == "__main__":
    cli()
