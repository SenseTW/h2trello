
import pytest
from sensetw.components import Hypothesis, Trello


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



if __name__ == "__main__":
    pytest.run([__file__])
