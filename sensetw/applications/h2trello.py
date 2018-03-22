
import os
import pickle

db_path = os.path.join(os.path.dirname(__file__), "../../db/h2trello.db")
def send(h, t, check_fn, limit=None):
    """
    Send Hypothesis annotations to Trello as cards.
    """
    inboxes = t.get_lists()
    labels = t.get_labels()

    sent_cards = []

    for card in h.annotations():
        if not check_fn(card):
            continue
        tid = t.post(card,
                     labels=[labels[card.source_type]
                             ] if card.source_type in labels else [],
                     list_id=inboxes[card.source_type])
        sent_cards.append(card)

        if limit is not None and len(sent_cards) >= limit:
            break

    return sent_cards



def save_log(log, filepath=None):
    if filepath is None:
        filepath = db_path
    with open(filepath, "wb") as fh:
        pickle.dump(log, fh)

def load_log(filepath=None):
    if filepath is None:
        filepath = db_path
    try:
        with open(filepath, "rb") as fh:
            return pickle.load(fh)
    except FileNotFoundError:
        return []

def find_log_by_trello_id(log, tid):
    for i, card in enumerate(log):
        if card.trello_id == tid:
            return i
    return -1


def find_log_by_hypothesis_id(log, hid):
    for i, card in enumerate(log):
        if card.hypothesis_id == hid:
            return i
    return -1

