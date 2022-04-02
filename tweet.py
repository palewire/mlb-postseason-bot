from datetime import datetime
import json

import click
from dateutil import parser as dateparse


@click.group
def cli():
    """Tweet the latest data."""
    pass


@cli.command()
def cubs():
    """Post the latest data."""
    standings = json.load(open("./data/standings.json", "r"))
    team_standings = next(t for t in standings['205']['teams'] if t['name'] == 'Chicago Cubs')

    schedule = json.load(open("./data/schedule.json", "r"))
    games_left = [g for g in schedule if not hasattr(g, "win_loss_result")]
    until_deadline = [g for g in games_left if dateparse.parse(g['date']) < datetime(2022, 8, 4)]

    projections = json.load(open("./data/fangraphs.json", "r"))

    message = f"""⚾🧮 @Cubs Status Report 🧮⚾

{team_standings['w']} wins
{team_standings['l']} losses

{len(games_left)} games left
{len(until_deadline)} games until the Aug. 3 trade deadline

{projections['Cubs']}% chance of making the postseason, according to @fangraphs
"""
    click.echo(message)


if __name__ == "__main__":
    cli()
