
import pytest
from sensetw.applications import h2trello
from sensetw import Card
import os

test_log_path = os.path.join(os.path.dirname(__file__), "h2trello.db")


@pytest.fixture
def h2trello_log():
    yield h2trello.load_log(filepath=test_log_path)
    try:
        os.remove(test_log_path)
    except FileNotFoundError:
        pass


def test_h2trello_log():
    log = h2trello.load_log(filepath=test_log_path)
    log.append(123)
    h2trello.save_log(log, filepath=test_log_path)

    log = h2trello.load_log(test_log_path)
    assert log == [123]

    os.remove(test_log_path)


def test_h2trello_log_find(h2trello_log):
    card = Card(
        title="", quote="",
        hypothesis_id="0", trello_id="1"
    )
    h2trello_log.append(card)

    r = h2trello.find_log_by_hypothesis_id(h2trello_log, "0")
    assert r == 0

    r = h2trello.find_log_by_hypothesis_id(h2trello_log, "1")
    assert r == -1

    r = h2trello.find_log_by_trello_id(h2trello_log, "1")
    assert r == 0


if __name__ == "__main__":
    pytest.run([__file__])
