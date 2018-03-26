
import requests
import csv
from sensetw.core import Mapping


def get_mappings(csv_url, agent=None):
    if agent is None:
        agent = requests
    response = agent.get(csv_url)
    contents = response.text.split("\n")
    reader = csv.DictReader(contents)
    return [Mapping(hypothesis_url=row["hypothesis_url"],
                    hypothesis_title=row["hypothesis_title"],
                    trello_url=row["trello_url"],
                    trello_title=row["trello_title"]) for row in reader]
