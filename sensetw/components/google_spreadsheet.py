
import requests
import csv

def get_mappings(csv_url, agent=None):
    if agent is None:
        agent = requests
    response = agent.get(csv_url)
    contents = response.text.split("\n")
    reader = csv.DictReader(contents)
    return [ dict(row) for row in reader ]
