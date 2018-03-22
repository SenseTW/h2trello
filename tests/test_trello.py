
import pytest
from sensetw.components import Trello
from sensetw import Card


@pytest.fixture
def t():
    return Trello(
        api_url="https://api.trello.com/1",
        api_key="foobarbaz",
        token="helloworld",
        title="",
        url="https://trello.com/b/Lo01hfDB/ai-foobarbaz")


def test_trello_board_id(t):
    assert t.board_id == "Lo01hfDB"


def test_trello_authorization(t):
    assert t.api_key == "foobarbaz"
    assert t.token == "helloworld"


def test_trello_comment_params(t):
    c = Card(comments=["123", "456"])
    c.trello_id = "abcedf"
    params = t.comment_params(c)
    assert len(params) == 2
    assert params[0]["id"] == "abcedf"
    assert params[0]["text"] == "123"
    assert params[1]["id"] == "abcedf"
    assert params[1]["text"] == "456"


if __name__ == "__main__":
    pytest.run([__file__])
