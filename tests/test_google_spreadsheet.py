
import pytest
from sensetw.components.google_spreadsheet import get_mappings

csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT7XQIbUWcchTC_1LGFrDa5gyVISkSriHQtKmfAuxhLkYX1KFkq9tzsbN0J7JTTf_z2yvfUr2g5_KPn/pub?gid=0&single=true&output=csv"

def test_get_mappings():
    mappings = get_mappings(csv_url)
    l = len(mappings)
    assert l > 0
    assert len(mappings[0].hypothesis_title) > 0
    assert len(mappings[0].hypothesis_url) > 0
    assert len(mappings[0].trello_title) > 0
    assert len(mappings[0].trello_url) > 0
