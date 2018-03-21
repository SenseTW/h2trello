
import re
import requests


class Trello:

    def __init__(self, api_url, api_key, token, title, url):
        self.api_url = api_url
        self.api_key = api_key
        self.token = token
        self.title = title
        self.url = url
        self._board_cache = {}

    def _request_board(self, objects, agent=None):
        if objects in self._board_cache:
            return self._board_cache[objects]
        if agent is None:
            agent = requests
        response = agent.get(
            self.api_url + "/boards/" + self.board_id + "/" + objects,
            params=self.request_params)
        self._board_cache[objects] = response.json()
        return self._board_cache[objects]

    def get_lists(self, agent=None):
        lists = self._request_board("lists")
        return {li["name"][8:]: li["id"] for li in lists
                if li["name"][:8] == "Inbox - "}

    def get_labels(self, agent=None):
        labels = self._request_board("labels")
        return {la["name"]: la["id"] for la in labels}

    def card_to_trello_card(self, card, labels=None, list_id=None):
        trello_name = "【{title}】{quote} {tags}".format(
            title=card.title,
            quote=card.quote,
            tags=" ".join(["#" + tag for tag in card.tags])
        )
        trello_desc = "\n".join(
            ["> " + line for line in card.quote.split("\n")]) \
            if card.quote is not None else ""
        trello_card = {
            "name": trello_name,
            "desc": trello_desc,
            "urlSource": card.source_url,
        }
        if labels is not None:
            trello_card["idLabels"] = ",".join(labels)
        if list_id is not None:
            trello_card["idList"] = list_id
        return trello_card

    def post(self, card, labels=None, list_id=None, agent=None):
        if agent is None:
            agent = requests
        params = {}
        params.update(self.request_params)
        params.update(self.card_to_trello_card(
            card, labels=labels, list_id=list_id))
        response = agent.post(self.api_url + "/cards", params=params)
        return response.text

    @property
    def board_id(self):
        board_re = re.compile("//trello.com/b/(.*?)/")
        r = board_re.search(self.url)
        return r.group(1)

    @property
    def request_params(self):
        return {"key": self.api_key, "token": self.token}
